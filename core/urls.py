from django.urls import path
from . import views
from . import admin_views
from django.urls import path

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_vievws
from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('impact/', views.ImpactView.as_view(), name='impact'),
    path('features/', views.FeaturesView.as_view(), name='features'),

    path('add/', views.AddTestimonialView.as_view(), name='add_testimonial'),  # URL to add testimonial
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),

   path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]