from django.contrib import admin
from .models import Article, ArticleCategory, Comment


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author_name', 'status', 'is_featured', 'view_count', 'published_at']
    list_filter = ['status', 'category', 'is_featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['user__username', 'body']
    list_editable = ['is_active']
