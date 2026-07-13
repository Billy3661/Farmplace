from django.contrib import admin
from .models import CourseCategory, Course, Module, Lesson, Enrollment, LessonCompletion


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'course_count']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'level', 'is_published', 'is_featured', 'enrollment_count']
    list_filter = ['category', 'level', 'is_published', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_free']
    list_filter = ['course', 'is_free']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'content_type', 'order', 'is_free']
    list_filter = ['module__course', 'content_type', 'is_free']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'progress', 'enrolled_at']
    list_filter = ['status']
    search_fields = ['user__username', 'course__title']


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed_at']
