from django.shortcuts import render
from . models import Article


def home(request):
    articles = Article.objects.filter(status='p').order_by('-publish')
    context = {
        "articles": articles
    }
    return render(request, "blog/home.html",context)


def detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        "article": article
    }
    return render(request, "blog/detail.html", context)
