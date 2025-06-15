from django.contrib import admin
from .models import Genre, Book, Exchange
from core.admin_actions import export_as_csv

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    actions = [export_as_csv]

class ExchangeInline(admin.TabularInline):
    model = Exchange
    extra = 0
    fields = ('requester', 'status', 'payment_completed', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'donor', 'location', 'is_available', 'created_at')
    list_filter = ('genre', 'is_available', 'delivery_option', 'created_at')
    search_fields = ('title', 'author', 'donor__username', 'donor_name', 'description')
    readonly_fields = ('created_at',)
    inlines = [ExchangeInline]
    actions = [export_as_csv]

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('book', 'requester', 'status', 'payment_completed', 'created_at')
    list_filter = ('status', 'payment_completed', 'created_at')
    search_fields = ('book__title', 'requester__username')
    readonly_fields = ('created_at',)
    actions = [export_as_csv]