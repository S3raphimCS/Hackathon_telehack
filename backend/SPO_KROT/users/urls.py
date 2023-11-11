from django.urls import path

from . import views

urlpatterns = [
   path('me/', views.me),
   path('rnd_pass/', views.create_random_password),
   path('signup/', views.signup_user),
]
