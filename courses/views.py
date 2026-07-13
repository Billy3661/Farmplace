from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, CourseCategory, Module, Lesson, Enrollment, LessonCompletion


def course_list(request):
    categories = CourseCategory.objects.filter(is_active=True)
    courses = Course.objects.filter(is_published=True)

    category_slug = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('q')

    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    featured_courses = Course.objects.filter(is_published=True, is_featured=True)[:3]

    context = {
        'courses': courses,
        'categories': categories,
        'featured_courses': featured_courses,
        'selected_category': category_slug,
        'selected_level': level,
        'search_query': search or '',
    }
    return render(request, 'courses/course_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug, is_active=True)
    courses = category.courses.filter(is_published=True)

    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'courses/category_detail.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    modules = course.modules.prefetch_related('lessons').all()
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

    context = {
        'course': course,
        'modules': modules,
        'enrollment': enrollment,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        course.enrollment_count += 1
        course.save(update_fields=['enrollment_count'])
        messages.success(request, f'You have been enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')

    return redirect('courses:course_learn', slug=slug)


@login_required
def course_learn(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    modules = course.modules.prefetch_related('lessons').all()
    completed_lessons = LessonCompletion.objects.filter(
        enrollment=enrollment
    ).values_list('lesson_id', flat=True)

    lesson_id = request.GET.get('lesson')
    current_lesson = None
    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    elif modules.exists() and modules.first().lessons.exists():
        current_lesson = modules.first().lessons.first()

    context = {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'completed_lessons': completed_lessons,
        'current_lesson': current_lesson,
    }
    return render(request, 'courses/course_learn.html', context)


@login_required
def complete_lesson(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    LessonCompletion.objects.get_or_create(
        enrollment=enrollment, lesson=lesson
    )
    enrollment.update_progress()

    messages.success(request, 'Lesson marked as complete!')

    next_lesson = Lesson.objects.filter(
        module__course=course, order__gt=lesson.order
    ).first()
    if next_lesson:
        return redirect(f'/courses/{slug}/learn/?lesson={next_lesson.id}')
    return redirect('courses:course_learn', slug=slug)
