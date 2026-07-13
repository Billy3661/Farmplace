from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent! We will get back to you shortly.')
            return redirect('contact:success')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': getattr(request.user, 'phone', ''),
            }
        form = ContactForm(initial=initial)

    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/success.html')
