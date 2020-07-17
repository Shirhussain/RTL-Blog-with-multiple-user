from django.urls import path, re_path
from .views import home, detail

app_name = "blog"
urlpatterns = [
    path('', home, name = "home"),
    re_path(r'article/(?P<slug>[-\w]+)/$', detail, name="detail"), # to do ( use $ )
]


