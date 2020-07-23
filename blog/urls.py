from django.urls import path, re_path
from .views import home, detail, category

app_name = "blog"
urlpatterns = [
    path('', home, name="home"),
    # this line is for pagination, i wanna show you like this ---> /page/5 instead of /?page=5
    path('page/<int:page>', home, name = "home"),
    re_path(r'article/(?P<slug>[-\w]+)/$', detail, name="detail"), # to do ( use $ )
    re_path(r'category/(?P<slug>[-\w]+)/$', category, name="category"), 
    re_path(r'category/(?P<slug>[-\w]+)/page/(?P<page>[0-9])/$', category, name="category"), 
]



