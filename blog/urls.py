from django.urls import path, re_path
from .views import ArticleView, ArticleDetail, CategoryView

app_name = "blog"
urlpatterns = [
    path('', ArticleView.as_view(), name="home"),
    # this line is for pagination, i wanna show you like this ---> /page/5 instead of /?page=5
    path('page/<int:page>', ArticleView.as_view(), name = "home"),
    re_path(r'article/(?P<slug>[-\w]+)/$', ArticleDetail.as_view(), name="detail"), # to do ( use $ )
    re_path(r'category/(?P<slug>[-\w]+)/$', CategoryView.as_view(), name="category"), 
    re_path(r'category/(?P<slug>[-\w]+)/page/(?P<page>[0-9])/$', CategoryView.as_view(), name="category"), 
]



