from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }
from django import forms

# class TestimonialForm(forms.ModelForm):
#     class Meta:
#         model = Testimonial
#         fields = ['name', 'role', 'content', 'image']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
#             'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Student, Teacher, Donor, etc.'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Share your experience with Books for All...'}),
#             'image': forms.FileInput(attrs={'class': 'form-control'}),
#         }