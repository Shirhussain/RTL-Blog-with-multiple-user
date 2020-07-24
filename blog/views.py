from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Article, Category

#for pageination i will put page=1 by default
# def home(request, page=1):
#     # using "Manager"--> published instead of filter(status='p')
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 8)
#     articles = paginator.get_page(page)

#     context = {
#         "articles": articles,
#     }
#     return render(request, "blog/home.html",context)

class ArticleView(ListView):
    # models = Article
    queryset = Article.objects.published()
    paginate_by = 10


# def detail(request, slug):
#     # article = get_object_or_404(Article, slug=slug, status='p')
#     # instead of above line i can use "Managers here"
#     article = get_object_or_404(Article.objects.published(), slug=slug)
#     context = {
#         "article": article
#     }
#     return render(request, "blog/detail.html", context)

class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 8)
#     articles = paginator.get_page(page)

#     context = {
#         "category": category,
#         "articles": articles
#     }
#     return render(request, "blog/category.html", context)

class CategoryView(ListView):
    paginate_by = 7
    template_name = "blog/category.html"

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context