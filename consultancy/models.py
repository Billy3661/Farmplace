from django.db import models
from django.conf import settings
from django.urls import reverse


class ConsultationService(models.Model):
    CATEGORY_CHOICES = [
        ('poultry', 'Poultry Consultancy'),
        ('piggery', 'Piggery Setup'),
        ('rabbit', 'Rabbit Farming'),
        ('goat', 'Goat & Sheep Farming'),
        ('dairy', 'Dairy Management'),
        ('vegetable', 'Vegetable Production'),
        ('business', 'Farm Business Planning'),
        ('biosecurity', 'Biosecurity Planning'),
        ('farm_visit', 'Farm Visits'),
        ('staff_training', 'Farm Staff Training'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='0 for quote-based')
    duration = models.CharField(max_length=50, blank=True, help_text='e.g. 2 hours, 1 day')
    is_online = models.BooleanField(default=True, help_text='Available online')
    is_in_person = models.BooleanField(default=True, help_text='Available in person')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Consultation Services'
        ordering = ['order', 'name']

    def __str__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse('consultancy:service_detail', kwargs={'pk': self.pk})


class ConsultationBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    TYPE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
        ('farm_visit', 'Farm Visit'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations')
    service = models.ForeignKey(ConsultationService, on_delete=models.CASCADE, related_name='bookings')
    consultation_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='online')
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    phone = models.CharField(max_length=15)
    farm_location = models.CharField(max_length=200, blank=True)
    description = models.TextField(help_text='Describe your farming situation or question')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    consultant_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.service.get_name_display()} ({self.status})"

    def get_absolute_url(self):
        return reverse('consultancy:booking_detail', kwargs={'pk': self.pk})
