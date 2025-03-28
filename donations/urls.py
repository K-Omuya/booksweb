from django.urls import path
from . import views

urlpatterns = [
    path('donate-book/', views.DonateBookView.as_view(), name='donate_book'),
    path('donate-money/', views.DonateMoneyView.as_view(), name='donate_money'),
    path('pledge/', views.PledgeDonationView.as_view(), name='pledge_donation'),
    path('success/', views.DonationSuccessView.as_view(), name='donation_success'),
    path('my-donations/', views.MyDonationsView.as_view(), name='my_donations'),
    path('pledge/success/', views.DonationSuccessView.as_view(), name='pledge_success'),
    path('payment-process/', views.payment_process, name='payment_process'),
]
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:  # Serve media only in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
