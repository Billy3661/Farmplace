from django.contrib import admin
from .models import ConsultationService, ConsultationBooking


@admin.register(ConsultationService)
class ConsultationServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'order']


@admin.register(ConsultationBooking)
class ConsultationBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'consultation_type', 'preferred_date', 'status']
    list_filter = ['status', 'consultation_type']
    search_fields = ['user__username', 'phone']
