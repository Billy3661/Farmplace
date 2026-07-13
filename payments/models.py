import base64
import datetime
import requests
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class PaymentManager(models.Manager):
    def get_successful(self):
        return self.filter(status='completed')


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    PURPOSE_CHOICES = [
        ('course_enrollment', 'Course Enrollment'),
        ('ebook_purchase', 'eBook Purchase'),
        ('membership', 'Membership Subscription'),
        ('chicks_order', 'Chicks Order'),
        ('consultancy', 'Consultancy Booking'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=15)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    reference_id = models.PositiveIntegerField(null=True, blank=True, help_text='ID of the related object')
    reference_model = models.CharField(max_length=50, blank=True, help_text='Model name of the related object')
    description = models.CharField(max_length=200, blank=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PaymentManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"KES {self.amount} - {self.user.username} ({self.status})"

    def get_absolute_url(self):
        return reverse('payments:payment_detail', kwargs={'pk': self.pk})


class MpesaGateway:
    """Safaricom Daraja API integration."""

    BASE_URL = 'https://sandbox.safaricom.co.ke'
    PRODUCTION_URL = 'https://api.safaricom.co.ke'

    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.is_production = not settings.DEBUG

    @property
    def base_url(self):
        return self.PRODUCTION_URL if self.is_production else self.BASE_URL

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            url,
            auth=(self.consumer_key, self.consumer_secret),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()['access_token']

    def generate_password(self, timestamp):
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(data_to_encode.encode()).decode('utf-8')

    def stk_push(self, phone, amount, account_reference, description):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        access_token = self.get_access_token()

        # Format phone number
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': str(int(amount)),
            'PartyA': phone,
            'PartyB': self.shortcode,
            'PhoneNumber': phone,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': description,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def query_status(self, checkout_request_id):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        access_token = self.get_access_token()

        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        return response.json()
