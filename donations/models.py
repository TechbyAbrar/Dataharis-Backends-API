from django.db import models
from django.core.validators import MinValueValidator


class Donation(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled')
    ]
    
    email = models.EmailField(blank=False, null=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])     # Ensures amount is >= 0
    payment_status = models.CharField(max_length=20, default='pending', choices=PAYMENT_STATUS_CHOICES)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Donation of ${self.amount} by {self.full_name or self.email} and your pay status is ({self.payment_status})"
