from django.contrib import admin
from .models import MembershipPlan, UserMembership


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'is_active']
    list_filter = ['is_active', 'duration_days']


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date']
    list_filter = ['status']
    search_fields = ['user__username']
