from django import forms
from .models import BookDonation, MonetaryDonation, DonationPledge

class BookDonationForm(forms.ModelForm):
    class Meta:
        model = BookDonation
        fields = ['title', 'author', 'book_type', 'quantity', 'description', 
                  'image', 'delivery_option', 'location', 'contact_email', 'contact_phone']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'book_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'delivery_option': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MonetaryDonationForm(forms.ModelForm):
    class Meta:
        model = MonetaryDonation
        fields = ['amount', 'anonymous', 'donor_name', 'donor_email', 'message']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 20}),
            'anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'donor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DonationPledgeForm(forms.ModelForm):
    class Meta:
        model = DonationPledge
        fields = ['book_quantity', 'monetary_amount', 'message', 'expected_date']
        widgets = {
            'book_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'monetary_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expected_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }