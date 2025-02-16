from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, full_name, email, country_code, mobile_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        full_mobile_number = f"{country_code}{mobile_number}"
        print(full_mobile_number)
        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            mobile_number=mobile_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, email, country_code, mobile_number, password):
        user = self.create_user(
            full_name=full_name,
            email=email,
            country_code=country_code,
            mobile_number=mobile_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            # RegexValidator(regex=r'^\d{10}$', message="Enter a valid mobile number. form models")
             RegexValidator(regex=r'^\+\d{1,4}\d{10}$', message="Enter a valid mobile number with country code.")
        ]
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile_number']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin




from django.db import models
from django.utils import timezone
import random

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = str(random.randint(100000, 999999)) 
        super().save(*args, **kwargs)
    
    def is_expired(self):
        # OTP expires in 5 minutes
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.mobile_number} - Verified: {self.is_verified}"
