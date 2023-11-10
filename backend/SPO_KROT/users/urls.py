from . import views
from django.urls import path


urlpatterns = [
   path('me/', views.me),
   path('rnd_pass/', views.create_random_password)
]
