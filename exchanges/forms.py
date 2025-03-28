from django import forms
from .models import Book, Exchange
from django import forms
from .models import Book
from django import forms
from .models import Book

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'genre', 'donor_name', 'contact_email', 
            'contact_phone', 'location', 'delivery_option', 'description', 
            'image', 'document' 
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_option': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = []