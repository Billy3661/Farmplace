from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from .models import Article, ArticleCategory, Comment


def article_list(request):
    articles = Article.objects.filter(status='published')
    categories = ArticleCategory.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    search = request.GET.get('q')

    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    if search:
        articles = articles.filter(title__icontains=search)

    paginator = Paginator(articles, 12)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    featured_article = Article.objects.filter(status='published', is_featured=True).first()

    context = {
        'articles': articles,
        'categories': categories,
        'featured_article': featured_article,
        'selected_category': category_slug,
        'search_query': search or '',
    }
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    article.view_count = F('view_count') + 1
    article.save(update_fields=['view_count'])

    comments = article.comments.filter(is_active=True)
    related_articles = Article.objects.filter(
        category=article.category, status='published'
    ).exclude(id=article.id)[:3]

    if request.method == 'POST' and request.user.is_authenticated:
        body = request.POST.get('body', '')
        if body:
            Comment.objects.create(
                article=article, user=request.user, body=body
            )
            messages.success(request, 'Comment added!')
            return redirect('blog:article_detail', slug=slug)

    context = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
    }
    return render(request, 'blog/article_detail.html', context)
