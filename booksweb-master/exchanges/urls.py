from django.urls import path
from . import views
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings  # ✅ Import settings
from django.conf.urls.static import static
from django.urls import path
from . import views  # Your app views


urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('upload/', views.BookUploadView.as_view(), name='book_upload'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),

    path('exchange/success/', TemplateView.as_view(template_name='exchanges/exchange_success.html'), name='exchange_success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
