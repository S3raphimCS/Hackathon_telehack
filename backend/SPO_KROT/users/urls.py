from django.urls import path

from . import admin, views

urlpatterns = [
   path('me/', views.me),
   path('rnd_pass/', views.create_random_password),
   path('signup/', admin.UserAdmin.signup, name='signup_user'),
   path('signup_with_api/', views.signup_user, name='api_signup_user')
]
