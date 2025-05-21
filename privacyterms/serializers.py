from rest_framework import serializers
from .models import PrivacyPolicy, TrustSafety, TermsConditions

class BaseContentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'description', 'last_updated']
        read_only_fields = ['id', 'last_updated']

class PrivacyPolicySerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = PrivacyPolicy

class TrustSafetySerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = TrustSafety

class TermsConditionsSerializer(BaseContentSerializer):
    class Meta(BaseContentSerializer.Meta):
        model = TermsConditions
