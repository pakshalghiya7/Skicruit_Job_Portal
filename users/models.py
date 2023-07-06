from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)

    email = models.EmailField(_('email address'), unique=True, max_length=100,
    error_messages={
    'unique': "A user with that email already exists.",
    })  
    is_employee = models.BooleanField(default=False)
    # is_employer = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    objects = CustomUserManager()
