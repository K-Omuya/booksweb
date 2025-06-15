from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactMessage, ImpactMetric
from .forms import ContactForm

from django.views.generic import TemplateView
from blogs.models import BlogPost  # Import BlogPost model
from core.models import ImpactMetric  # Import ImpactMetric model

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metrics'] = ImpactMetric.objects.all()  # Fetch all impact metrics
        context['featured_posts'] = BlogPost.objects.filter(is_featured=True, is_published=True).order_by('-created_at')[:3]  # Fetch latest 3 featured posts
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['testimonials'] = Testimonial.objects.filter(is_active=True)
        context['metrics'] = ImpactMetric.objects.all()
        return context

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)


# Impact View
class ImpactView(TemplateView):
    template_name = 'core/impact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metrics'] = ImpactMetric.objects.all()
        
        # Additional statistics and data can be added here
        context['total_books'] = 15000  # Example hardcoded value
        context['total_students'] = 5000  # Example hardcoded value
        context['total_schools'] = 30  # Example hardcoded value
        context['total_clubs'] = 25  # Example hardcoded value
        
        return context

# Features View
class FeaturesView(TemplateView):
    template_name = 'core/features.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define features to display
        context['features'] = [
            {
                'title': 'Book Exchanges',
                'description': 'Exchange your books with others in the community. For a small fee of 20 shillings, facilitate the exchange of knowledge.',
                'icon': 'fas fa-exchange-alt'
            },
            {
                'title': 'Book Donations',
                'description': 'Donate your books to students and schools in need. Help provide educational resources to those who need them most.',
                'icon': 'fas fa-hand-holding-heart'
            },
            {
                'title': 'Book Clubs',
                'description': 'Join or create book clubs in primary schools that help collect, catalog, and distribute books.',
                'icon': 'fas fa-users'
            },
            {
                'title': 'Monetary Donations',
                'description': 'Support our mission by making monetary donations to help us purchase new books and expand our reach.',
                'icon': 'fas fa-money-bill-wave'
            },
            {
                'title': 'Educational Blogs',
                'description': 'Access educational content and stay updated with the latest news and trends in education.',
                'icon': 'fas fa-blog'
            },
            {
                'title': 'Impact Tracking',
                'description': 'Track our impact and see how your contributions are making a difference in the lives of students.',
                'icon': 'fas fa-chart-line'
            }
        ]
        
        return context



from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.db.models import Sum, Count
from exchanges.models import Book, Exchange
from clubs.models import BookClub
from donations.models import BookDonation
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate impact metrics from database
        # 1. Students Impacted (using User count as a proxy)
        students_impacted = User.objects.count()
        
        # 2. Schools Reached (using BookClub count)
        schools_reached = BookClub.objects.count()
        
        # 3. Books Exchanged (count of completed exchanges)
        books_exchanged = Exchange.objects.filter(status='completed').count()
        
        # 4. Books Donated (count of book donations)
        books_donated = BookDonation.objects.count()
        
        # Create impact metrics list
        metrics = [
            {'title': 'Students Impacted', 'value': students_impacted, 'icon': 'fa-users'},
            {'title': 'Schools Reached', 'value': schools_reached, 'icon': 'fa-school'},
            {'title': 'Books Exchanged', 'value': books_exchanged, 'icon': 'fa-exchange-alt'},
            {'title': 'Books Donated', 'value': books_donated, 'icon': 'fa-hand-holding-heart'}
        ]
        
        context['metrics'] = metrics
        
        # Add other context data as needed
        return context


from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView
from .models import ContactMessage, Testimonial, ImpactMetric
from .forms import ContactForm, TestimonialForm
from django.urls import reverse_lazy
from django.contrib import messages

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        context['metrics'] = ImpactMetric.objects.all()
        return context


# views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from .models import Testimonial
from .forms import TestimonialForm

from django.shortcuts import render
from .forms import TestimonialForm

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Testimonial
from .forms import TestimonialForm

class AddTestimonialView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'core/add_testimonial.html'
    success_url = reverse_lazy('testimonials')  # Redirects to testimonials page after form submission

    def form_valid(self, form):
        form.instance.is_active = False  # Set to inactive by default for moderation
        # Display a success message
        messages.success(self.request, 'Thank you for your testimonial! It will be displayed after review by the Books for All team.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for field in context['form']:
            field.field.widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class manually
        return context


# View to display all active (approved) testimonials
def testimonials_view(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'core/testimonials.html', {'testimonials': testimonials})


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Add any context data needed for the dashboard
    context = {
        'user': request.user,
        # Add other context variables as needed
    }
    
    return render(request, 'core/dashboard.html', context)    



