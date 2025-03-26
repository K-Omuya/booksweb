from django.urls import path
from . import views

from django.views.generic import TemplateView
urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('upload/', views.BookUploadView.as_view(), name='book_upload'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),

    path('exchange/success/', TemplateView.as_view(template_name='exchanges/exchange_success.html'), name='exchange_success'),

]