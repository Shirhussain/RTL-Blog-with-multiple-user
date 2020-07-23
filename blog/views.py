from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def home(request):
    # using "Manager"--> published instead of filter(status='p')
    articles = Article.objects.published()
    context = {
        "articles": articles,
    }
    return render(request, "blog/home.html",context)


def detail(request, slug):
    # article = get_object_or_404(Article, slug=slug, status='p')
    # instead of above line i can use "Managers here"
    article = get_object_or_404(Article.objects.published(), slug=slug)
    context = {
        "article": article
    }
    return render(request, "blog/detail.html", context)


def category(request, slug):
    context = {
        "category":get_object_or_404(Category, slug=slug,status=True)
    }
    return render(request, "blog/category.html", context)
    
