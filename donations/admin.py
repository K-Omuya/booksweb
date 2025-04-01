from django.contrib import admin
from .models import BookDonation, MonetaryDonation, DonationPledge

@admin.register(BookDonation)
class BookDonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'book_type', 'quantity', 'location', 'created_at')
    list_filter = ('book_type', 'delivery_option', 'created_at')
    search_fields = ('title', 'author', 'donor__username', 'description')
    readonly_fields = ('created_at',)

@admin.register(MonetaryDonation)
class MonetaryDonationAdmin(admin.ModelAdmin):
    list_display = ('get_donor_display', 'amount', 'transaction_id', 'is_completed', 'created_at')
    list_filter = ('anonymous', 'is_completed', 'created_at')
    search_fields = ('donor__username', 'donor_name', 'donor_email', 'transaction_id')
    readonly_fields = ('created_at',)

    def get_donor_display(self, obj):
        if obj.anonymous:
            return 'Anonymous'
        elif obj.donor:
            return obj.donor.username
        else:
            return obj.donor_name
    get_donor_display.short_description = 'Donor'

@admin.register(DonationPledge)
class DonationPledgeAdmin(admin.ModelAdmin):
    list_display = ('donor', 'book_quantity', 'monetary_amount', 'fulfilled', 'expected_date', 'created_at')
    list_filter = ('fulfilled', 'created_at')
    search_fields = ('donor__username', 'message')
    readonly_fields = ('created_at',)