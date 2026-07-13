from django.db import models
from django.urls import reverse
from django.conf import settings


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon name')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Course Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courses:category_detail', kwargs={'slug': self.slug})

    @property
    def course_count(self):
        return self.courses.filter(is_published=True).count()


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text='e.g. 4 weeks')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    instructor = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    enrollment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    @property
    def module_count(self):
        return self.modules.count()

    @property
    def lesson_count(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def has_discount(self):
        return self.original_price and self.original_price > self.price


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False, help_text='Allow free preview')

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    @property
    def lesson_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text Notes'),
        ('video', 'Video'),
        ('poster', 'Poster/Image'),
        ('document', 'Document'),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True, help_text='Rich text content for the lesson')
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    poster = models.ImageField(upload_to='courses/posters/', blank=True, null=True)
    notes_file = models.FileField(upload_to='courses/notes/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=50, blank=True, help_text='e.g. 15 min')
    is_free = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    @property
    def is_downloadable(self):
        return bool(self.notes_file)


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    progress = models.PositiveIntegerField(default=0, help_text='Percentage 0-100')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    @property
    def is_completed(self):
        return self.status == 'completed'

    def update_progress(self):
        total_lessons = Lesson.objects.filter(module__course=self.course).count()
        if total_lessons == 0:
            self.progress = 0
        else:
            completed = LessonCompletion.objects.filter(
                enrollment=self, lesson__module__course=self.course
            ).count()
            self.progress = int((completed / total_lessons) * 100)
        self.save()


class LessonCompletion(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='completions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment} - {self.lesson}"
