from django.urls import path

from . import views

urlpatterns = [
   path('create_report/', views.create_report),
   path('reports/', views.ReportListView.as_view(), name='reports'),
   path('report/<int:pk>', views.ReportDetailView.as_view(), name='report'),
   path('report/<int:pk>/edit', views.update_report_metrics, name='update_metric'),
   path('report/upload/', views.ExcelUploadView.as_view(), name='file_download'),
   path('report/search/', views.ReportSearchView.as_view(), name='search'),
   path('report/me', views.my_reports, name='my_reports')
]
