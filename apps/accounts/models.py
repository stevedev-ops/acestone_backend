from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'OWNER')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Boss / Owner'
        EMPLOYEE = 'EMPLOYEE', 'Sales Consultant / Employee'
        MANAGER = 'MANAGER', 'Store Manager'

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    phone = models.CharField(max_length=30, blank=True)
    pin_code = models.CharField(max_length=6, blank=True, help_text='4-digit authorization PIN for Boss/Manager')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0300)
    avatar_url = models.URLField(max_length=500, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def is_owner(self):
        return self.role == self.Role.OWNER

    def is_manager(self):
        return self.role == self.Role.MANAGER

    def is_employee(self):
        return self.role == self.Role.EMPLOYEE

