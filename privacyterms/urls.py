from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrivacyPolicyViewSet,
    TrustSafetyViewSet,
    TermsConditionsViewSet
)

router = DefaultRouter()
router.register(r'privacy-policy', PrivacyPolicyViewSet)
router.register(r'trust-safety', TrustSafetyViewSet)
router.register(r'terms-conditions', TermsConditionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
