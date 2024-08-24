from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('profile/', views.ProfilePageView.as_view(), name='profile-page')
]
