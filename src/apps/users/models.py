from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Link to the custom manager
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(validators=[URLValidator()], blank=True)
    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    account_status = models.CharField(max_length=10, choices=[(
        'Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')], default='Active')
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
