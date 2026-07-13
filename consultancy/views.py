from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConsultationService, ConsultationBooking
from .forms import ConsultationBookingForm


def consultancy_list(request):
    services = ConsultationService.objects.filter(is_active=True)
    return render(request, 'consultancy/consultancy_list.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(ConsultationService, pk=pk, is_active=True)
    return render(request, 'consultancy/service_detail.html', {'service': service})


@login_required
def book_consultation(request, pk):
    service = get_object_or_404(ConsultationService, pk=pk, is_active=True)

    if request.method == 'POST':
        form = ConsultationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            messages.success(request, 'Your consultation has been booked! We will confirm shortly.')
            return redirect('consultancy:booking_detail', pk=booking.pk)
    else:
        form = ConsultationBookingForm(initial={'phone': getattr(request.user, 'phone', '')})

    return render(request, 'consultancy/book_consultation.html', {
        'service': service, 'form': form,
    })


@login_required
def booking_list(request):
    bookings = ConsultationBooking.objects.filter(user=request.user)
    return render(request, 'consultancy/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(ConsultationBooking, pk=pk, user=request.user)
    return render(request, 'consultancy/booking_detail.html', {'booking': booking})
