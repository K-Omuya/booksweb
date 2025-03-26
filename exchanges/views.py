from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Book, Exchange, Genre
from .forms import BookUploadForm, ExchangeRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class BookListView(ListView):
    model = Book
    template_name = 'exchanges/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_available=True)
        genre = self.request.GET.get('genre')
        query = self.request.GET.get('q')
        
        if genre:
            queryset = queryset.filter(genre__name=genre)
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query) | 
                models.Q(author__icontains=query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
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
