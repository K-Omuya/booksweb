from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from .models import BookDonation, MonetaryDonation, DonationPledge
from .forms import BookDonationForm, MonetaryDonationForm, DonationPledgeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages




class DonateBookView(LoginRequiredMixin, CreateView):
    model = BookDonation
    form_class = BookDonationForm
    template_name = 'donations/donate_book.html'
    success_url = reverse_lazy('donation_success')
    
    def form_valid(self, form):
        form.instance.donor = self.request.user
        messages.success(self.request, 'Thank you for your book donation!')
        return super().form_valid(form)

class DonateMoneyView(CreateView):
    model = MonetaryDonation
    form_class = MonetaryDonationForm
    template_name = 'donations/donate_money.html'
    success_url = reverse_lazy('payment_process')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated and not form.instance.anonymous:
            form.instance.donor = self.request.user
        messages.success(self.request, 'Thank you for your generous donation!')
        return super().form_valid(form)


class PledgeDonationView(LoginRequiredMixin, CreateView):
    model = DonationPledge
    form_class = DonationPledgeForm
    template_name = 'donations/pledge.html'
    success_url = reverse_lazy('pledge_success')
    
    def form_valid(self, form):
        form.instance.donor = self.request.user
        messages.success(self.request, 'Thank you for your pledge! Your commitment makes a difference.')
        return super().form_valid(form)

class DonationSuccessView(TemplateView):
    template_name = 'donations/pledge_success.html'

class MyDonationsView(LoginRequiredMixin, ListView):
    template_name = 'donations/my_donations.html'
    context_object_name = 'donations'
    
    def get_queryset(self):
        user = self.request.user
        book_donations = BookDonation.objects.filter(donor=user)
        money_donations = MonetaryDonation.objects.filter(donor=user)
        pledges = DonationPledge.objects.filter(donor=user)
        
        return {
            'books': book_donations,
            'money': money_donations,
            'pledges': pledges
        }
def payment_process(request):
    if request.method == 'POST':
        # Get the donation data from session or form data
        form = MonetaryDonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.donor = request.user
            
            # Save to session for now (we'll save to DB after successful payment)
            request.session['donation_data'] = {
                'amount': float(donation.amount),
                'payment_method': donation.payment_method,
                'phone_number': getattr(donation, 'phone_number', ''),
                'anonymous': donation.anonymous,
                'donor_name': donation.donor_name,
                'donor_email': donation.donor_email,
                'message': donation.message
            }
            
            # For the template to access
            context = {'donation': donation}
            return render(request, 'donations/payment_process.html', context)
    
    # If not POST or form invalid, redirect back to donation page
    return redirect('donate_money')