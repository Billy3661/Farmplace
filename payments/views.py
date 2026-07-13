from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Payment, MpesaGateway


@login_required
def initiate_payment(request, purpose, reference_id):
    """Initiate M-Pesa STK Push payment."""
    if request.method != 'POST':
        return redirect('home')

    phone = request.POST.get('phone', '')
    amount = request.POST.get('amount', '0')

    if not phone or not amount:
        messages.error(request, 'Phone number and amount are required.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    try:
        amount = float(amount)
    except ValueError:
        messages.error(request, 'Invalid amount.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        amount=amount,
        phone=phone,
        purpose=purpose,
        reference_id=reference_id,
        status='pending',
    )

    # Initiate STK Push
    try:
        mpesa = MpesaGateway()
        account_ref = f"FP-{purpose[:3].upper()}-{payment.id}"
        response = mpesa.stk_push(
            phone=phone,
            amount=amount,
            account_reference=account_ref,
            description=f"FarmPlace - {purpose.replace('_', ' ').title()}",
        )

        if response.get('ResponseCode') == '0':
            payment.checkout_request_id = response.get('CheckoutRequestID', '')
            payment.status = 'processing'
            payment.save(update_fields=['checkout_request_id', 'status'])
            messages.info(request, 'Please check your phone for the M-Pesa prompt.')
        else:
            payment.status = 'failed'
            payment.save(update_fields=['status'])
            messages.error(request, 'Failed to initiate payment. Please try again.')

    except Exception as e:
        payment.status = 'failed'
        payment.save(update_fields=['status'])
        messages.error(request, 'Payment service unavailable. Please try again later.')

    return redirect('payments:payment_detail', pk=payment.pk)


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    return render(request, 'payments/payment_detail.html', {'payment': payment})


@csrf_exempt
@require_POST
def mpesa_callback(request):
    """Handle M-Pesa callback from Safaricom."""
    try:
        data = json.loads(request.body)
        result = data.get('Body', {}).get('stkCallback', {})

        result_code = result.get('ResultCode')
        result_desc = result.get('ResultDesc', '')
        checkout_id = result.get('CheckoutRequestID', '')

        payment = Payment.objects.filter(checkout_request_id=checkout_id).first()
        if not payment:
            return JsonResponse({'result': 'ok'})

        if result_code == 0:
            # Payment successful
            metadata = result.get('CallbackMetadata', {}).get('Item', [])
            receipt = next(
                (item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber'),
                ''
            )
            payment.mpesa_receipt = receipt
            payment.status = 'completed'
            payment.save(update_fields=['mpesa_receipt', 'status'])

            # Trigger post-payment actions
            _process_successful_payment(payment)
        else:
            payment.status = 'failed'
            payment.save(update_fields=['status'])

    except Exception:
        pass

    return JsonResponse({'result': 'ok'})


@login_required
def payment_status(request, pk):
    """AJAX endpoint to check payment status."""
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    return JsonResponse({
        'status': payment.status,
        'receipt': payment.mpesa_receipt,
    })


def _process_successful_payment(payment):
    """Process post-payment actions based on purpose."""
    from courses.models import Course, Enrollment
    from ebooks.models import Ebook, EbookPurchase
    from membership.models import MembershipPlan, UserMembership
    from chicks.models import ChickOrder

    if payment.purpose == 'course_enrollment' and payment.reference_id:
        course = Course.objects.filter(id=payment.reference_id).first()
        if course:
            Enrollment.objects.get_or_create(
                user=payment.user, course=course,
                defaults={'status': 'active'}
            )
            course.enrollment_count += 1
            course.save(update_fields=['enrollment_count'])

    elif payment.purpose == 'ebook_purchase' and payment.reference_id:
        ebook = Ebook.objects.filter(id=payment.reference_id).first()
        if ebook:
            EbookPurchase.objects.get_or_create(
                user=payment.user, ebook=ebook,
                defaults={'payment_reference': payment.mpesa_receipt}
            )
            ebook.download_count += 1
            ebook.save(update_fields=['download_count'])

    elif payment.purpose == 'membership' and payment.reference_id:
        plan = MembershipPlan.objects.filter(id=payment.reference_id).first()
        if plan:
            UserMembership.create_or_extend(
                user=payment.user, plan=plan,
                receipt=payment.mpesa_receipt
            )

    elif payment.purpose == 'chicks_order' and payment.reference_id:
        order = ChickOrder.objects.filter(id=payment.reference_id).first()
        if order:
            order.status = 'confirmed'
            order.save(update_fields=['status'])
