from django.shortcuts import render
from . models import Article


def home(request):
    articles = Article.objects.all()
    context = {
        "articles": articles
    }
    for article in articles:
        print(article.title)
    return render(request, "blog/home.html",context)


def detail(request, slug):
    return render(request, "blog/detail.html", {})
