from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
      Custom User model that extends Django's built-in AbstractUser model.

      This model adds additional fields like email, activation_token.
      It also changes the default username field to an email field.
      """
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=50, blank=True, null=True, default='ghost', verbose_name="Username")
    activation_token = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="images/users/", blank=True, null=True, verbose_name="Image")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_manager(self):
        return self.groups.filter(name='content-manager').exists()
