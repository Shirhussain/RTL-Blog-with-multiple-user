from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Article, Category

#for pageination i will put page=1 by default
def home(request, page=1):
    # using "Manager"--> published instead of filter(status='p')
    articles_list = Article.objects.published()
    paginator = Paginator(articles_list, 8)
    articles = paginator.get_page(page)

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


def category(request, slug, page=1):
    category = get_object_or_404(Category, slug=slug, status=True)
    articles_list = category.articles.published()
    paginator = Paginator(articles_list, 8)
    articles = paginator.get_page(page)

    context = {
        "category": category,
        "articles": articles
    }
    return render(request, "blog/category.html", context)
    
