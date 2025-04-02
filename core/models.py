from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class ImpactMetric(models.Model):
    title = models.CharField(max_length=100)
    value = models.IntegerField()
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title


# models.py
from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Default is False for moderation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
