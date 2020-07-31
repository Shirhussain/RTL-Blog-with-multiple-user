from django.http import Http404

# The same code is sused by djano it self as well in django.admin.contrib.auth.mixin
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["author", "title","slug", "category", "description", "thumbnail", "publish", "status"]
        elif request.user.is_author:
            self.fields = ["title", "slug", "category", "description", "thumbnail", "publish"]
        else:
            raise Http404("به شما اجازه دسترسی به این آدرس نیست")
        return super().dispatch(request, *args, **kwargs)

# I wnna submit The author name automatically when he/she submited the article 

# class FormValidMxin():
#     # i wanna overwrite the form_valid()
#     # the passed form here is that one which somebuddy gonna create the article
#     def form_valid(self, form):
#         # by default django use 'form.save()' 
#         if self.request.user.is_superuser:
#             form.save()
#         else:
#             self.obj = form.save(commit=False)
#             self.obj.author = self.request.user
#             self.obj.status = "d"
#         return super().form_valid(form)


class FormValidMxin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = "d"
        return super().form_valid(form)

