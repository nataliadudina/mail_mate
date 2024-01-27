from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.urls import reverse_lazy

from users.models import User


def activate_user(activation_token):
    user = get_object_or_404(User, activation_token=activation_token)
    user.is_active = True
    user.activation_token = None
    user.save()
    return user


def send_activation_email(request: HttpRequest, user):
    # Builds the absolute URI for the activation link
    activation_url = request.build_absolute_uri(
        reverse_lazy('users:activate', args=[user.activation_token]))

    # Sends an email to the user with the activation link
    send_mail(
        subject='Welcome to Mail Mate! Activate Your Account!',
        message=f'Thank you for registering! To activate your account click on the following link:\n\n{activation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
