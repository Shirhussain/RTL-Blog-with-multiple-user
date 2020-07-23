from django.urls import path, re_path
from .views import home, detail, category

app_name = "blog"
urlpatterns = [
    path('', home, name = "home"),
    re_path(r'article/(?P<slug>[-\w]+)/$', detail, name="detail"), # to do ( use $ )
    re_path(r'category/(?P<slug>[-\w]+)/$', category, name="category"), # to do ( use $ )
]



