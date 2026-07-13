from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Q
from .models import Ebook, EbookCategory, EbookPurchase, EbookDownload


def ebook_list(request):
    categories = EbookCategory.objects.filter(is_active=True)
    ebooks = Ebook.objects.filter(is_published=True)

    category_slug = request.GET.get('category')
    search = request.GET.get('q')

    if category_slug:
        ebooks = ebooks.filter(category__slug=category_slug)
    if search:
        ebooks = ebooks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    featured_ebooks = Ebook.objects.filter(is_published=True, is_featured=True)[:4]

    context = {
        'ebooks': ebooks,
        'categories': categories,
        'featured_ebooks': featured_ebooks,
        'selected_category': category_slug,
        'search_query': search or '',
    }
    return render(request, 'ebooks/ebook_list.html', context)


def ebook_detail(request, slug):
    ebook = get_object_or_404(Ebook, slug=slug, is_published=True)
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = EbookPurchase.objects.filter(
            user=request.user, ebook=ebook
        ).exists()

    related_ebooks = Ebook.objects.filter(
        category=ebook.category, is_published=True
    ).exclude(id=ebook.id)[:4]

    context = {
        'ebook': ebook,
        'has_purchased': has_purchased,
        'related_ebooks': related_ebooks,
    }
    return render(request, 'ebooks/ebook_detail.html', context)


@login_required
def purchase_ebook(request, slug):
    ebook = get_object_or_404(Ebook, slug=slug, is_published=True)

    if EbookPurchase.objects.filter(user=request.user, ebook=ebook).exists():
        messages.info(request, 'You have already purchased this eBook.')
        return redirect('ebooks:ebook_download', slug=slug)

    # Redirect to M-Pesa payment
    return redirect('payments:ebook_payment', ebook_id=ebook.id)


@login_required
def download_ebook(request, slug):
    ebook = get_object_or_404(Ebook, slug=slug, is_published=True)
    purchase = get_object_or_404(EbookPurchase, user=request.user, ebook=ebook)

    EbookDownload.objects.create(
        purchase=purchase,
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    if ebook.file:
        response = FileResponse(ebook.file.open('rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{ebook.title}.pdf"'
        return response

    messages.error(request, 'File not available at the moment.')
    return redirect('ebooks:ebook_detail', slug=slug)
