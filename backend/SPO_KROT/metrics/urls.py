from django.urls import path

from . import views

urlpatterns = [
   path('create_report/', views.create_report),
]
