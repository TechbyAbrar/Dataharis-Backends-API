from django.db import models
from accounts.models import UserAuth
# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True, default="No Title by User")
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return  f"This '{self.title[:30]}...' is posted by {self.author}"


class MsPost(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, default="No Title by Author")
    image = models.ImageField(upload_to='adminpost/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title[:30]}... is posted by Admin"