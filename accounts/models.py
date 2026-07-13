from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_farmer = models.BooleanField(default=True)
    is_consultant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse('accounts:profile')


class FarmerProfile(models.Model):
    FARM_TYPE_CHOICES = [
        ('poultry', 'Poultry'),
        ('piggery', 'Piggery'),
        ('rabbit', 'Rabbit'),
        ('goat', 'Goat & Sheep'),
        ('dairy', 'Dairy'),
        ('beef', 'Beef'),
        ('crops', 'Crops'),
        ('mixed', 'Mixed Farming'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    county = models.CharField(max_length=50, blank=True)
    sub_county = models.CharField(max_length=50, blank=True)
    farm_name = models.CharField(max_length=100, blank=True)
    farm_type = models.CharField(max_length=20, choices=FARM_TYPE_CHOICES, blank=True)
    farm_size = models.CharField(max_length=50, blank=True, help_text='e.g. 2 acres, 500 birds')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Farmer Profile'
        verbose_name_plural = 'Farmer Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_absolute_url(self):
        return reverse('accounts:profile')

    @property
    def display_name(self):
        return self.farm_name or self.user.get_full_name() or self.user.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'
