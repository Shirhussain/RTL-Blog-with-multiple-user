from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from blog.models import Article

@login_required
def home(request):
    return render(request, "registration/home.html")

class ArticleView(LoginRequiredMixin, ListView):
    template_name = "registration/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)
            
    
class ArticleCreate(LoginRequiredMixin ,CreateView):
    model = Article
    template_name = "registration/article_create_update.html"
    fields = ["author", "title","slug", "category", "description", "thumbnail", "publish", "status"]
    def get_success_url(self):
        return reverse("account:home")
        

    