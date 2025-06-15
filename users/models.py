from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# models.py
from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    ACTIONS = (
        ('add', 'Add'),
        ('change', 'Change'),
    )

    ACTIVITY_CHOICES = (
        ('blog_post', 'Blog Post'),
        ('comment', 'Comment'),
        ('club', 'Club'),
        ('club_activity', 'Club Activity'),
        ('county', 'County'),
        ('contact_message', 'Contact Message'),
        ('impact_metric', 'Impact Metric'),
        ('book_donation', 'Book Donation'),
        ('donation_pledge', 'Donation Pledge'),
        ('monetary_donation', 'Monetary Donation'),
        ('exchange', 'Exchange'),
        ('genre', 'Genre'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    action = models.CharField(max_length=10, choices=ACTIONS)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_activity_type_display()} - {self.get_action_display()} - {self.timestamp}"
