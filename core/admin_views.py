# Create the admin_views.py file in the core app

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from exchanges.models import Book, Exchange
from donations.models import BookDonation, MonetaryDonation
from clubs.models import BookClub
from blogs.models import BlogPost

@staff_member_required
def admin_dashboard(request):
    # Get statistics for summary cards
    total_users = User.objects.count()
    total_books = Book.objects.count()
    total_book_donations = BookDonation.objects.count()
    total_monetary_donations = MonetaryDonation.objects.filter(is_completed=True).aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_exchanges = Exchange.objects.filter(status='completed').count()
    total_clubs = BookClub.objects.count()
    total_blog_posts = BlogPost.objects.count()
    
    # Get data for line chart - registrations over time
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get user registrations by day for the last 30 days
    user_registrations = []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        count = User.objects.filter(date_joined__date=day).count()
        user_registrations.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Get books added by day for the last 30 days
    books_added = []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        count = Book.objects.filter(created_at__date=day).count()
        books_added.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Get donations by day for the last 30 days
    donations = []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        count = BookDonation.objects.filter(created_at__date=day).count()
        donations.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Get recent activity
    recent_registrations = User.objects.order_by('-date_joined')[:5]
    recent_books = Book.objects.order_by('-created_at')[:5]
    recent_donations = BookDonation.objects.order_by('-created_at')[:5]
    recent_exchanges = Exchange.objects.order_by('-created_at')[:5]
    
    context = {
        'title': 'Admin Dashboard',
        'total_users': total_users,
        'total_books': total_books,
        'total_book_donations': total_book_donations,
        'total_monetary_donations': total_monetary_donations,
        'total_exchanges': total_exchanges,
        'total_clubs': total_clubs,
        'total_blog_posts': total_blog_posts,
        'user_registrations': user_registrations,
        'books_added': books_added,
        'donations': donations,
        'recent_registrations': recent_registrations,
        'recent_books': recent_books,
        'recent_donations': recent_donations,
        'recent_exchanges': recent_exchanges,
    }
    
    return render(request, 'admin/dashboard.html', context)
