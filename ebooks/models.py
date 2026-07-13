from django.db import models
from django.urls import reverse
from django.conf import settings


class EbookCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'eBook Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def ebook_count(self):
        return self.ebooks.filter(is_published=True).count()


class Ebook(models.Model):
    category = models.ForeignKey(EbookCategory, on_delete=models.CASCADE, related_name='ebooks')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, default='FarmPlace Team')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cover_image = models.ImageField(upload_to='ebooks/covers/', blank=True, null=True)
    file = models.FileField(upload_to='ebooks/files/')
    pages = models.PositiveIntegerField(default=0)
    file_size = models.CharField(max_length=20, blank=True, help_text='e.g. 2.5 MB')
    language = models.CharField(max_length=20, default='English')
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ebooks:ebook_detail', kwargs={'slug': self.slug})

    @property
    def has_discount(self):
        return self.original_price and self.original_price > self.price


class EbookPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ebook_purchases')
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['user', 'ebook']
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.user.username} - {self.ebook.title}"


class EbookDownload(models.Model):
    purchase = models.ForeignKey(EbookPurchase, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-downloaded_at']

    def __str__(self):
        return f"Download: {self.purchase}"
