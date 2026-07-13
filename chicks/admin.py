from django.contrib import admin
from .models import ChickType, ChickBatch, ChickOrder


@admin.register(ChickType)
class ChickTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']


@admin.register(ChickBatch)
class ChickBatchAdmin(admin.ModelAdmin):
    list_display = ['chick_type', 'age', 'quantity_available', 'price_per_bird', 'is_active']
    list_filter = ['chick_type', 'age', 'is_active']


@admin.register(ChickOrder)
class ChickOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'batch', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'batch__chick_type']
    search_fields = ['user__username', 'full_name', 'phone']
