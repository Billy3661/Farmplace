from django.contrib import admin
from .models import EbookCategory, Ebook, EbookPurchase, EbookDownload


@admin.register(EbookCategory)
class EbookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'is_published', 'is_featured', 'download_count']
    list_filter = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(EbookPurchase)
class EbookPurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'ebook', 'purchased_at']
    search_fields = ['user__username', 'ebook__title']


@admin.register(EbookDownload)
class EbookDownloadAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'downloaded_at']
