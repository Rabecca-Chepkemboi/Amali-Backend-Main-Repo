from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField



class RegistrationManager(BaseUserManager):
    def create_user(self, email, password,**other_fields,):
        if not email:
            raise ValueError(_("You must provide a valid email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **other_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name =models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password =models.CharField(max_length=200)
    role = models.CharField(max_length=255, default='regular_user')
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS= ['password']
    USERNAME_FIELD = 'email'
    objects=RegistrationManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Athlete(models.Model):
    full_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.PositiveIntegerField()

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    achievements = models.TextField()
    phone_number = PhoneNumberField(blank=True)  
    role = models.CharField(max_length=20, default='athlete')

class Sponsor(models.Model):
    full_name =models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password =models.CharField(max_length=32)
    Organisation = models.CharField(max_length=255, null=True)
    Bio = models.TextField()
    phone_number = PhoneNumberField( blank=True, null=False, default= None)
    role = models.CharField(max_length=20, default='sponsor')
