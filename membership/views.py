from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MembershipPlan, UserMembership


def membership_plans(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    user_membership = None
    if request.user.is_authenticated:
        user_membership = UserMembership.objects.filter(user=request.user).first()

    context = {
        'plans': plans,
        'user_membership': user_membership,
    }
    return render(request, 'membership/membership_plans.html', context)


@login_required
def subscribe(request, plan_slug):
    plan = MembershipPlan.objects.get(slug=plan_slug, is_active=True)

    # Redirect to M-Pesa payment
    return redirect('payments:initiate_payment', purpose='membership', reference_id=plan.id)


@login_required
def membership_status(request):
    membership = UserMembership.objects.filter(user=request.user).first()
    return render(request, 'membership/membership_status.html', {'membership': membership})
