from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from register.models import Sponsor, Athlete

class Donation(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE, default="")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sponsors = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='sponsored_donations', default="")
    

    def __str__(self):
        return f"Amount: {self.amount} Donation from {self.sponsors} to {self.athlete}"


    class Meta:
        verbose_name_plural = "Donations"