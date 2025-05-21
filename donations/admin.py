from django.contrib import admin
from .models import Donation
# Register your models here.

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'amount', 'payment_status', 'stripe_session_id', 'created_at']
    list_filter = ('payment_status', 'created_at')
    search_fields = ('email', 'full_name', 'location')
    
    
