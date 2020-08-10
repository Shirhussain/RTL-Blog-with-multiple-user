from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView

from blog.models import Article
from . models import User
from . forms import UserForm
from .mixins import FieldsMixin, FormValidMxin, AuthorAccessMixin,AuthorsAccessMixin, SuperUserAccessMixin


@login_required
def home(request):
    return render(request, "registration/home.html")

class ArticleView(AuthorsAccessMixin, ListView):
    template_name = "registration/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)
            
    
class ArticleCreate(AuthorsAccessMixin, FieldsMixin,FormValidMxin, CreateView):
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


class Profile(LoginRequiredMixin, UpdateView):
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

#here i determine that diffrent type of user should have diffrent login url 
#e.g: superuser and author should redirect to account home and other user to profile
class Login(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")


# i need success url but for default 'PsswordChangeView' i can't add myapp 'account:profile' in django soruce
# so i have to overwrite the passwordChangeView as fallows
# class PasswordChange(PasswordChangeView):
#     success_url = reverse_lazy("account:password_change_done")




from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})


# here is another way i wanna use class base view instead of function base view
class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('برای تایید حساب تان به شما ایمل شده است ایمل تان را چک کنید و بعد از تایید وارید شوید.<a href="/login">ورود</a>')

# now it's the time to activate the link after user clicked on the link
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
		# her it says that login the use after accont activation but somebody don't wanna do that 
		# instead the wanna login the use again with basic login so that time you can remove the line bellow
		# as i do

        # login(request, user)
        # return redirect('home')
        return HttpResponse('حساب شما با موفقیت فعال شد برای ورود <a href="/login">کلیک</a> کنید.')
    else:
        return HttpResponse('لینک فعال سازی معتبر نیست یا منقضی شده است. <a href="/registration">دوباره امتحان کنید</a>')