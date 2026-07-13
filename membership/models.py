from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class MembershipPlan(models.Model):
    DURATION_CHOICES = [
        (30, 'Monthly'),
        (365, 'Annual'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(choices=DURATION_CHOICES)
    features = models.JSONField(default=list, help_text='List of feature strings')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']

    def __str__(self):
        return f"{self.name} - KES {self.price}"

    @property
    def monthly_equivalent(self):
        if self.duration_days >= 365:
            return round(float(self.price) / 12, 0)
        return float(self.price)

    @property
    def savings_percentage(self):
        if self.duration_days >= 365:
            monthly_price = MembershipPlan.objects.filter(
                duration_days=30, is_active=True
            ).first()
            if monthly_price:
                annual_monthly = float(self.price) / 12
                savings = ((float(monthly_price.price) - annual_monthly) / float(monthly_price.price)) * 100
                return int(savings)
        return 0


class UserMembership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='membership')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else 'No Plan'} ({self.status})"

    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()

    @property
    def days_remaining(self):
        if self.end_date > timezone.now():
            return (self.end_date - timezone.now()).days
        return 0

    @property
    def membership_tier(self):
        if not self.is_active:
            return 'Free'
        if self.plan and self.plan.duration_days >= 365:
            return 'Gold'
        return 'Silver'

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    @classmethod
    def create_or_extend(cls, user, plan, receipt=''):
        membership, created = cls.objects.get_or_create(
            user=user,
            defaults={
                'plan': plan,
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=plan.duration_days),
                'payment_reference': receipt,
            }
        )
        if not created:
            # Extend existing membership
            if membership.end_date < timezone.now():
                membership.start_date = timezone.now()
            membership.end_date = membership.end_date + timedelta(days=plan.duration_days)
            membership.plan = plan
            membership.status = 'active'
            membership.payment_reference = receipt
            membership.save()
        return membership

    def check_expiry(self):
        if self.end_date <= timezone.now():
            self.status = 'expired'
            self.save(update_fields=['status'])
