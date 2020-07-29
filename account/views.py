from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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
            
    
