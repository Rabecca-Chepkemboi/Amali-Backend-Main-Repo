from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class Donation(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def save(self, *args, **kwargs):
        if self.payment_confirmed():
            self.status = self.CONFIRMED
        else:
            self.status = self.PENDING

        super().save(*args, **kwargs)
    
    def payment_confirmed(self):
        return self.amount > 0 and self.status  




