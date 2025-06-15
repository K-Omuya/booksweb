from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book, Exchange, Genre
from .forms import BookUploadForm, ExchangeRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Book, Genre
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class BookListView(ListView):
    model = Book
    template_name = 'exchanges/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_available=True)
        
        # Get filter parameters from request
        genre_id = self.request.GET.get('genre')
        location = self.request.GET.get('location')
        book_type = self.request.GET.get('type')
        search_query = self.request.GET.get('q')
        
        # Apply filters if they exist
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        
        if location:
            queryset = queryset.filter(location=location)
        
        if book_type:
            if book_type == 'donation':
                queryset = queryset.filter(is_donation=True)
            elif book_type == 'exchange':
                queryset = queryset.filter(is_donation=False)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(author__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add genres for filter dropdown
        context['genres'] = Genre.objects.all()
        
        # Add unique locations for filter dropdown
        locations = Book.objects.filter(is_available=True).values_list('location', flat=True).distinct()
        context['locations'] = sorted(locations)
        
        return context

# For donation books specifically
class DonationBookListView(BookListView):
    def get_queryset(self):
        # Start with the parent queryset but always filter for donations
        queryset = super().get_queryset().filter(is_donation=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Change the title to indicate these are donation books
        context['page_title'] = "Donated Books"
        context['is_donation_page'] = True
        return context
class BookDetailView(DetailView):
    model = Book
    template_name = 'exchanges/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = ExchangeRequestForm()
        return context

class BookUploadView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookUploadForm
    template_name = 'exchanges/book_upload.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        form.instance.donor = self.request.user
        messages.success(self.request, 'Your book has been uploaded successfully!')
        return super().form_valid(form)

class MyBooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'exchanges/my_books.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.filter(donor=self.request.user)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib import messages
from .models import Book, Exchange
from .forms import ExchangeRequestForm

class BookDetailView(DetailView):
    model = Book
    template_name = 'exchanges/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = ExchangeRequestForm()
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to request a book exchange.")
            return redirect('login')
        
        self.object = self.get_object()
        form = ExchangeRequestForm(request.POST)
        
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.book = self.object
            exchange.requester = request.user
            exchange.status = 'pending'
            exchange.save()
            
            messages.success(request, "Your exchange request has been submitted successfully!")
            return redirect('exchange_success')  # Redirect to success page
        else:
            context = self.get_context_data(object=self.object, form=form)
            return self.render_to_response(context)
