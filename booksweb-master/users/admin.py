from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone_number', 'birth_date')
    list_filter = ('location', 'birth_date')
    search_fields = ('user__username', 'user__email', 'location', 'phone_number', 'bio')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'location', 'birth_date', 'phone_number', 'profile_picture')
        }),
    )