from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
class Book(models.Model):
    DELIVERY_CHOICES = (
        ('pickup', 'Personal Pickup'),
        ('dropoff', 'Drop Off Location'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100)
    delivery_option = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    document = models.FileField(upload_to='books/documents/', blank=True, null=True)  # ✅ Handles document uploads
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Exchange(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.requester.username} - {self.book.title}"
