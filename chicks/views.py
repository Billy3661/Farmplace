from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import ChickType, ChickBatch, ChickOrder
from .forms import ChickOrderForm


def chicks_catalog(request):
    chick_types = ChickType.objects.filter(is_active=True).prefetch_related('batches')
    available_batches = ChickBatch.objects.filter(
        quantity_available__gt=0, is_active=True
    ).select_related('chick_type')

    context = {
        'chick_types': chick_types,
        'available_batches': available_batches,
    }
    return render(request, 'chicks/catalog.html', context)


def chick_type_detail(request, breed):
    chick_type = get_object_or_404(ChickType, name=breed, is_active=True)
    batches = chick_type.batches.filter(is_active=True)

    context = {
        'chick_type': chick_type,
        'batches': batches,
    }
    return render(request, 'chicks/type_detail.html', context)


@login_required
def order_chicks(request, batch_id):
    batch = get_object_or_404(ChickBatch, id=batch_id, is_active=True)

    if not batch.is_available:
        messages.error(request, 'This batch is no longer available.')
        return redirect('chicks:catalog')

    if request.method == 'POST':
        form = ChickOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.batch = batch
            order.total_price = batch.price_per_bird * order.quantity

            if order.quantity > batch.quantity_available:
                messages.error(request, f'Only {batch.quantity_available} birds available.')
                return redirect('chicks:order_chicks', batch_id=batch_id)

            order.save()

            # Reduce available quantity
            batch.quantity_available -= order.quantity
            batch.save(update_fields=['quantity_available'])

            # Redirect to payment
            return redirect('payments:initiate_payment', purpose='chicks_order', reference_id=order.id)
    else:
        initial = {
            'full_name': request.user.get_full_name(),
            'phone': getattr(request.user, 'phone', ''),
            'email': request.user.email,
        }
        form = ChickOrderForm(initial=initial)

    context = {
        'batch': batch,
        'form': form,
    }
    return render(request, 'chicks/order_form.html', context)


@login_required
def order_list(request):
    orders = ChickOrder.objects.filter(user=request.user)

    context = {
        'orders': orders,
    }
    return render(request, 'chicks/order_list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(ChickOrder, pk=pk, user=request.user)

    context = {
        'order': order,
    }
    return render(request, 'chicks/order_detail.html', context)
