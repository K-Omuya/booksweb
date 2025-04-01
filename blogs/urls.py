from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/new/', views.BlogCreateView.as_view(), name='blog_create'),
    path('<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]