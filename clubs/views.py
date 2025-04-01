from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import BookClub, ClubActivity, County
from .forms import BookClubForm, ClubActivityForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class BookClubListView(ListView):
    model = BookClub
    template_name = 'clubs/club_list.html'
    context_object_name = 'clubs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = BookClub.objects.filter(is_active=True)
        county = self.request.GET.get('county')
        
        if county:
            queryset = queryset.filter(county__name=county)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counties'] = County.objects.all()
        return context

class BookClubDetailView(DetailView):
    model = BookClub
    template_name = 'clubs/club_detail.html'
    context_object_name = 'club'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = self.object.activities.all().order_by('-date')
        return context

class BookClubCreateView(LoginRequiredMixin, CreateView):
    model = BookClub
    form_class = BookClubForm
    template_name = 'clubs/club_create.html'
    success_url = reverse_lazy('club_list')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Your book club has been created successfully!')
        return super().form_valid(form)

class ClubActivityCreateView(LoginRequiredMixin, CreateView):
    model = ClubActivity
    form_class = ClubActivityForm
    template_name = 'clubs/activity_create.html'
    
    def get_success_url(self):
        return reverse_lazy('club_detail', kwargs={'pk': self.kwargs['club_id']})
    
    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(BookClub, pk=self.kwargs['club_id'])
        if self.club.creator != request.user:
            messages.error(request, 'You do not have permission to add activities to this club.')
            return redirect('club_detail', pk=self.club.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.club = self.club
        messages.success(self.request, 'Activity added successfully!')
        return super().form_valid(form)