from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookClubListView.as_view(), name='club_list'),
    path('<int:pk>/', views.BookClubDetailView.as_view(), name='club_detail'),
    path('create/', views.BookClubCreateView.as_view(), name='club_create'),
    path('<int:club_id>/add-activity/', views.ClubActivityCreateView.as_view(), name='activity_create'),
]