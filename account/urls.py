from django.contrib.auth import views
from django.urls import path
from .views import home, ArticleView, ArticleCreate, ArticleUpdate, ArticleDelete, Profile, Login

app_name = 'account'

    # i don't need this path anymore because i wanna sue default django path[summary]
# urlpatterns = [
    
#     path('logout/', views.LogoutView.as_view(), name='logout'),

#     path('password_change/', PasswordChange.as_view(), name='password_change'),
#     path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

#     path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]

# urlpatterns += [
urlpatterns = [
    # path('', home, name='home'),
    path('', ArticleView.as_view(), name="home"),
    path('profile/', Profile.as_view(), name = "profile"),
    path('articles/create/', ArticleCreate.as_view(), name="article_create"),
    path('articles/update/<int:pk>/', ArticleUpdate.as_view(), name="article_update"),
    path('articles/delete/<int:pk>/', ArticleDelete.as_view(), name="article_delete"),
]