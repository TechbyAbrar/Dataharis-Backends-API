from rest_framework import viewsets
from .models import PrivacyPolicy, TrustSafety, TermsConditions
from .serializers import (
    PrivacyPolicySerializer, 
    TrustSafetySerializer, 
    TermsConditionsSerializer
)
from blogs.permissions import IsSuperUserOrReadOnly

class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [IsSuperUserOrReadOnly]

class TrustSafetyViewSet(viewsets.ModelViewSet):
    queryset = TrustSafety.objects.all()
    serializer_class = TrustSafetySerializer
    permission_classes = [IsSuperUserOrReadOnly]

class TermsConditionsViewSet(viewsets.ModelViewSet):
    queryset = TermsConditions.objects.all()
    serializer_class = TermsConditionsSerializer
    permission_classes = [IsSuperUserOrReadOnly]
