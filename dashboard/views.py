from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from courses.models import Enrollment
from ebooks.models import EbookPurchase
from membership.models import UserMembership
from chicks.models import ChickOrder
from payments.models import Payment
from blog.models import Article


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'home/index.html')


@login_required
def dashboard_home(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    membership = UserMembership.objects.filter(user=user).first()

    # Unsliced querysets for stats
    all_enrollments = Enrollment.objects.filter(user=user)
    all_ebook_purchases = EbookPurchase.objects.filter(user=user)
    all_chick_orders = ChickOrder.objects.filter(user=user)

    # Sliced querysets for display
    enrollments = all_enrollments.select_related('course')[:5]
    ebook_purchases = all_ebook_purchases.select_related('ebook')[:5]
    chick_orders = all_chick_orders.select_related('batch', 'batch__chick_type')[:5]
    recent_payments = Payment.objects.filter(user=user)[:5]

    total_spent = Payment.objects.filter(
        user=user, status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0

    active_courses = all_enrollments.filter(status='active').count()
    completed_courses = all_enrollments.filter(status='completed').count()

    days_remaining = 0
    if membership and membership.is_active:
        days_remaining = membership.days_remaining

    stats = {
        'total_courses': all_enrollments.count(),
        'active_courses': active_courses,
        'completed_courses': completed_courses,
        'total_ebooks': all_ebook_purchases.count(),
        'total_orders': all_chick_orders.count(),
        'total_spent': total_spent,
        'membership_days': days_remaining,
    }

    context = {
        'profile': profile,
        'membership': membership,
        'enrollments': enrollments,
        'ebook_purchases': ebook_purchases,
        'chick_orders': chick_orders,
        'recent_payments': recent_payments,
        'stats': stats,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def dashboard_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'dashboard/courses.html', {'enrollments': enrollments})


@login_required
def dashboard_ebooks(request):
    purchases = EbookPurchase.objects.filter(user=request.user).select_related('ebook')
    return render(request, 'dashboard/ebooks.html', {'purchases': purchases})


@login_required
def dashboard_orders(request):
    orders = ChickOrder.objects.filter(user=request.user).select_related('batch', 'batch__chick_type')
    return render(request, 'dashboard/orders.html', {'orders': orders})


@login_required
def dashboard_payments(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'dashboard/payments.html', {'payments': payments})
