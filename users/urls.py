from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserRegistrationView, UserProfileView, UserLoginView, EmailConfirmationView

app_name = 'OnlineStore_users'


urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('confirm/<str:email>/<uuid:confirmation_code>/', EmailConfirmationView.as_view(), name='email_confirmation'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
