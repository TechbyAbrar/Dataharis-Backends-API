from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class PrivacyPolicy(BaseContent):
    pass

class TrustSafety(BaseContent):
    pass

class TermsConditions(BaseContent):
    pass
