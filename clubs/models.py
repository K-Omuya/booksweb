from django.db import models
from django.conf import settings

class County(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Counties"

class BookClub(models.Model):
    name = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    student_count = models.PositiveIntegerField()
    patron_name = models.CharField(max_length=100)
    patron_contact = models.CharField(max_length=20)
    patron_email = models.EmailField()
    description = models.TextField(blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.school_name}"

class ClubActivity(models.Model):
    club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='club_activities/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.club.name} - {self.title}"
    
    class Meta:
        verbose_name_plural = "Club Activities"