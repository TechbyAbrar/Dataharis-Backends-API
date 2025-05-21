from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from accounts.manager import UserManager
import random
import string

class UserAuth(AbstractBaseUser,PermissionsMixin):
    class Meta:
        verbose_name_plural = "User"
    email = models.EmailField(max_length=100,unique=True)
    full_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='faces/', default='faces/profile.png',null=True,blank=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    mobile_no = models.CharField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expired = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def generate_otp(self):
        otp = ''.join(random.choices(string.digits, k=6))
        self.otp = otp
        self.otp_expired = timezone.now() + timedelta(minutes=5)
        self.save()
        return otp