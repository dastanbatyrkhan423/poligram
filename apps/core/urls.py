from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('certificates/', views.CertificatesView.as_view(), name='certificates'),
    path('licenses/', views.LicensesView.as_view(), name='licenses'),
    path('all-services/', views.AllServicesView.as_view(), name='all_services'),
]
