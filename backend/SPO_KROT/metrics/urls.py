from django.urls import path

from . import views

urlpatterns = [
   path('create_report/', views.create_report),
   path('reports/', views.ReportListView.as_view(), name='reports'),
   path('report/<int:pk>', views.ReportDetailView.as_view(), name='report'),
   path('report/<int:pk>/edit', views.update_report_metrics, name='update-metric')
]