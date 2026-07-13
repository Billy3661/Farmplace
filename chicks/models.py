from django.db import models
from django.conf import settings
from django.urls import reverse


class ChickType(models.Model):
    BREED_CHOICES = [
        ('kenbro', 'Kenbro'),
        ('sasso', 'Sasso'),
        ('sussex', 'Sussex'),
    ]

    name = models.CharField(max_length=50, choices=BREED_CHOICES, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='chicks/types/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_name_display()

    @property
    def available_batches(self):
        return self.batches.filter(quantity_available__gt=0, is_active=True)


class ChickBatch(models.Model):
    AGE_CHOICES = [
        ('day_old', 'Day-old'),
        ('one_week', '1 Week'),
        ('two_weeks', '2 Weeks'),
        ('three_weeks', '3 Weeks'),
        ('one_month', '1 Month'),
    ]

    chick_type = models.ForeignKey(ChickType, on_delete=models.CASCADE, related_name='batches')
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    quantity_available = models.PositiveIntegerField(default=0)
    price_per_bird = models.DecimalField(max_digits=10, decimal_places=2)
    batch_code = models.CharField(max_length=50, blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['age', '-created_at']
        unique_together = ['chick_type', 'age', 'batch_code']

    def __str__(self):
        return f"{self.chick_type.get_name_display()} - {self.get_age_display()} (KES {self.price_per_bird})"

    @property
    def is_available(self):
        return self.quantity_available > 0 and self.is_active

    @property
    def total_value(self):
        return self.quantity_available * self.price_per_bird


class ChickOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Collection'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chick_orders')
    batch = models.ForeignKey(ChickBatch, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    county = models.CharField(max_length=50)
    sub_county = models.CharField(max_length=50)
    delivery_address = models.TextField()
    preferred_delivery_date = models.DateField(null=True, blank=True)
    needs_brooding_guide = models.BooleanField(default=True)
    needs_vaccination_schedule = models.BooleanField(default=True)
    special_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('chicks:order_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.batch.price_per_bird * self.quantity
        super().save(*args, **kwargs)

    @property
    def chick_breed(self):
        return self.batch.chick_type.get_name_display()

    @property
    def chick_age(self):
        return self.batch.get_age_display()
