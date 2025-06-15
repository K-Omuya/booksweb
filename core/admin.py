from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from .models import ContactMessage,  ImpactMetric

# Configure the admin site
admin.site.site_header = 'Books for All Administration'
admin.site.site_title = 'Books for All Admin'
admin.site.index_title = 'Dashboard'

# Register core models
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = ('name', 'role', 'is_active')
#     list_filter = ('is_active',)
#     search_fields = ('name', 'role', 'content')
#     list_editable = ('is_active',)

@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon')
    search_fields = ('title',)

# Add shortcuts to the admin index
class BookAdmin(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        
        return app_list
# admin.py
from django.contrib import admin
from .models import Testimonial

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'created_at')
    list_filter = ('is_active',)  # Filter by active or inactive testimonials
    search_fields = ('name', 'role', 'content')  # Enable search by name, role, or content
    actions = ['approve_testimonials']  # Add custom actions to approve testimonials

    def approve_testimonials(self, request, queryset):
        """Custom action to approve selected testimonials."""
        queryset.update(is_active=True)
        self.message_user(request, "Selected testimonials have been approved.")

    approve_testimonials.short_description = "Approve selected testimonials"

admin.site.register(Testimonial, TestimonialAdmin)
