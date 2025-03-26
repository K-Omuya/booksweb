from django.urls import path
from . import views
from . import admin_views
from django.urls import path




urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('impact/', views.ImpactView.as_view(), name='impact'),
    
    # Features URLs
    path('features/', views.FeaturesView.as_view(), name='features'),



    


]