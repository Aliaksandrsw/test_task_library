from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views


app_name = "users"


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reader/register/', views.RegisterReader.as_view(), name='register_reader'),
    path('librian/register/', views.RegisterLibrian.as_view(), name='register_lib'),
]