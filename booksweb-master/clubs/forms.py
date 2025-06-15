from django import forms
from .models import BookClub, ClubActivity

class BookClubForm(forms.ModelForm):
    class Meta:
        model = BookClub
        fields = ['name', 'school_name', 'county', 'student_count', 
                  'patron_name', 'patron_contact', 'patron_email', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'county': forms.Select(attrs={'class': 'form-control'}),
            'student_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'patron_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patron_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'patron_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ClubActivityForm(forms.ModelForm):
    class Meta:
        model = ClubActivity
        fields = ['title', 'description', 'date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }