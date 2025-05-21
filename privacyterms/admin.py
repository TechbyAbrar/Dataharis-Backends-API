from django.contrib import admin
from .models import PrivacyPolicy, TrustSafety, TermsConditions
# Register your models here.

@admin.register(PrivacyPolicy)
class PrivacyAndPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(TrustSafety)
class TrustAndSafetyAdmin(admin.ModelAdmin):
    list_display = ['title','description']

@admin.register(TermsConditions)
class TermsAndConditionAdmin(admin.ModelAdmin):
    list_display = ['title','description']