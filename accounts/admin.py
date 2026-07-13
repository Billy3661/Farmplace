from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FarmerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_farmer', 'is_active']
    list_filter = ['is_farmer', 'is_consultant', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('FarmPlace', {'fields': ('phone', 'is_farmer', 'is_consultant')}),
    )


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'farm_name', 'farm_type', 'county', 'years_experience']
    list_filter = ['farm_type', 'county']
    search_fields = ['user__username', 'farm_name', 'county']
