from django.urls import path
from . import views
from .views import autosuggest
urlpatterns = [
    # path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path('logout', views.logout, name='logout'),
    path("add_patient/", views.add_patient, name="add_patient"),
    path("add_patient_report/", views.add_patient_report, name="add_patient_report"),
    path("patient_list/", views.patient_list, name="patient_list"),
    path("patient_report/<int:id>", views.patient_report, name="patient_report"),
    path("patient/<str:pk>", views.patient, name="patient"),
    path("autosuggest/", views.autosuggest, name="autosuggest"),
    path("autodoctor/", views.autodoctor, name="autodoctor"),
    path("info/", views.info, name="info"),
    path('view_report/<int:rid>/', views.view_report.as_view(), name="view_report"),
    # path('DownloadReportasPDF/<int:rid>/', views.DownloadReportasPDF.as_view(), name="DownloadReportasPDF"),
    path('DownloadReportasPDF/<int:rid>/', views.DownloadReportasPDF, name="DownloadReportasPDF"),
    # path('preview_reportt/<int:rid>/', views.preview_report, name="preview_report")
]
