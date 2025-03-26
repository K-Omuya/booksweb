from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ContactMessage, ImpactMetric
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        context['metrics'] = ImpactMetric.objects.all()
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

# # Testimonial Views
# class TestimonialListView(ListView):
#     model = Testimonial
#     template_name = 'core/testimonial_list.html'
#     context_object_name = 'testimonials'
#     queryset = Testimonial.objects.filter(is_active=True)
#     paginate_by = 9

# class TestimonialDetailView(DetailView):
#     model = Testimonial
#     template_name = 'core/testimonial_detail.html'
#     context_object_name = 'testimonial'

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


# class TestimonialsListView(ListView):
#     model = Testimonial
#     template_name = 'core/testimonials.html'
#     context_object_name = 'testimonials'
#     paginate_by = 9
    
#     def get_queryset(self):
#         # Only show approved testimonials to the public
#         return Testimonial.objects.filter(is_active=True).order_by('-created_at')

# class TestimonialCreateView(CreateView):
#     model = Testimonial
#     form_class = TestimonialForm
#     template_name = 'core/testimonial_form.html'
#     success_url = reverse_lazy('testimonials')
    
#     def form_valid(self, form):
#         # Set is_active to False so admin can review
#         form.instance.is_active = False
#         messages.success(self.request, 'Thank you for your testimonial! It will be reviewed and published soon.')
#         return super().form_valid(form)