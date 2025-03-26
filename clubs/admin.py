from django.contrib import admin
from .models import County, BookClub, ClubActivity

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ClubActivityInline(admin.TabularInline):
    model = ClubActivity
    extra = 0

@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_name', 'county', 'student_count', 'patron_name', 'is_active', 'created_at')
    list_filter = ('county', 'is_active', 'created_at')
    search_fields = ('name', 'school_name', 'patron_name', 'description')
    readonly_fields = ('created_at',)
    inlines = [ClubActivityInline]

@admin.register(ClubActivity)
class ClubActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'description', 'club__name')