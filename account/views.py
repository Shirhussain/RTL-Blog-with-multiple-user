from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Article
from . models import User
from . forms import UserForm
from .mixins import FieldsMixin, FormValidMxin, AuthorAccessMixin, SuperUserAccessMixin


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
            
    
class ArticleCreate(LoginRequiredMixin, FieldsMixin,FormValidMxin, CreateView):
    model = Article
    template_name = "registration/article_create_update.html"
    # the following line (fields) is working but if you wanna have diffrent user wiht different access 
    # so i have to use Mixin and create a file by the name of mixins.py for that in account 
    # and bring The 'FieldsMixin' instead here
    # fields = ["author", "title","slug", "category", "description", "thumbnail", "publish", "status"]
    
    def get_success_url(self):
        return reverse("account:home")

#her i don't need LoginRequiredMixin anymore because i define Atuhor Access mixin so here we go
class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMxin, UpdateView):
    model = Article
    template_name = "registration/article_create_update.html"

    def get_success_url(self):
        return reverse("account:home")
        

class ArticleDelete(SuperUserAccessMixin,DeleteView):
    model = Article
    success_url = reverse_lazy("account:home")
    template_name = "registration/article_confirm_delete.html"


class Profile(UpdateView):
    model = User
    form_class = UserForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("account:profile")

    # here i wanna detemine that author can only edite their own profile 
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    #by default when we disabled some fileds for profile form in form it effect on superuser as well 
    # her i wanna exclude The Superuser, so i have to connect throw 'kwargs'
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
        