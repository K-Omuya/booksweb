from django.db import models
from django.conf import settings

class BookDonation(models.Model):
    BOOK_TYPES = (
        ('curriculum', 'Curriculum Books'),
        ('story', 'Story Books'),
        ('general', 'General Reading Books'),
    )
    
    DELIVERY_CHOICES = (
        ('dropoff', 'Drop Off at School'),
        ('pickup', 'Arrange for Pickup'),
    )
    
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    delivery_option = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    location = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.quantity} books"

class MonetaryDonation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    anonymous = models.BooleanField(default=False)
    donor_name = models.CharField(max_length=100, blank=True)
    donor_email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.anonymous:
            return f"Anonymous - {self.amount}"
        elif self.donor:
            return f"{self.donor.username} - {self.amount}"
        else:
            return f"{self.donor_name} - {self.amount}"

class DonationPledge(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_quantity = models.PositiveIntegerField(default=0)
    monetary_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    message = models.TextField(blank=True)
    fulfilled = models.BooleanField(default=False)
    expected_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.donor.username} - Books: {self.book_quantity}, Money: {self.monetary_amount}"