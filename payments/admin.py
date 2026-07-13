from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'phone', 'purpose', 'status', 'mpesa_receipt', 'created_at']
    list_filter = ['status', 'purpose', 'created_at']
    search_fields = ['user__username', 'mpesa_receipt', 'phone']
    readonly_fields = ['created_at', 'updated_at']
