from django.shortcuts import render, get_object_or_404
from . models import Article


def home(request):
    articles = Article.objects.filter(status='p').order_by('-publish')
    context = {
        "articles": articles
    }
    return render(request, "blog/home.html",context)


def detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='p')
    context = {
        "article": article
    }
    return render(request, "blog/detail.html", context)
