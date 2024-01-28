from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class NameAuthBackend(BaseBackend):
    """Custom authentication backend that allows users
    to authenticate using their either username or email"""
    def authenticate(self, request, username=None, password=None, **kwargs):    # Authenticates the given credentials
        user_model = get_user_model()
        try:
            if '@' in username:  # Checks if the entered string is an email
                user = user_model.objects.get(email=username)
            else:
                user = user_model.objects.get(username=username)

            # Checks if the password matches the user's password
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    # Returns the User object for the given user ID
    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
