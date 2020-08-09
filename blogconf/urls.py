from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login


urlpatterns = [
    # because of diffrent user type of login url i will use that one which i have define myself
    # path('login/', views.LoginView.as_view(), name='login'),
    path('login/', Login.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('account.urls', namespace='account')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
