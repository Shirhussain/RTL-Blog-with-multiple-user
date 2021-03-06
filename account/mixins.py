from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article
# The same code is sused by djano it self as well in django.admin.contrib.auth.mixin
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_superuser:
        #     self.fields = ["author", "title","slug", "category", "description", "thumbnail", "publish","is_special","status"]
        # elif request.user.is_author:
        #     self.fields = ["title", "slug", "category", "description", "thumbnail","is_special", "publish"]
        # else:
        #     raise Http404("به شما اجازه دسترسی به این آدرس نیست")
        
        # after i decide that author also has access to send for investigation the article so i removed the above code
        # and use below code
        self.fields = ["title", "slug", "category", "description", "thumbnail", "publish", "is_special", "status"]
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


# I wnna submit The author name automatically when he/she submited the article 
class FormValidMxin():
    # i wanna overwrite the form_valid()
    # the passed form here is that one which somebuddy gonna create the article
    def form_valid(self, form):
        # by default django use 'form.save()' 
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            # self.obj.status = "d"
            
            # the next code is the restrict the author for publishing the article 
            # also i could use like this code as well ---> if not self.obj.status in ['i','d']: 
            if not self.obj.status == "i":
                self.obj.status = "d"
        return super().form_valid(form)


#for ArticleUpdate there is a bug if some author wanna edite from other other 
#by changing the 'pk' in url can ealsy change the article but i wnna prevent by mixin 
class AuthorAccessMixin():
    def dispatch(self, request,pk, *args, **kwargs):
        # first of all i have to get the Article then chack the author of Article 
        article = get_object_or_404(Article, pk=pk)
        # here i wanna restrict that author can edite only draft articles except superuser
        # instead of status =="d and b " we need to create a list like following
        if article.author == request.user and article.status in ['b','d'] or request.user.is_superuser:
            return super().dispatch(request,*args, **kwargs)
        else:
            raise  Http404("شما اجازه دسترسی به این آدرس را ندارید")


#i wanna restrict some url like 'article_list, article_crate or update ' for nornal user 
class AuthorsAccessMixin():
    #author mixin take 'pk' and apply onley for one author but here is for diffrent type of author
        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser or request.user.is_author:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    return redirect("account:profile")
            else:
                return redirect("login")
# To make sure that only superuser hass access to delete so i do it like this 
class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما اجازه دسترسی به این آدرس را ندارید")
        