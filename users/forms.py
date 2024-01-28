from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.html import format_html


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email: ', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Username: ", required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="*Password: ", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="*Confirm password: ", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': '*E-mail: ',
            'first_name': 'First name: ',
            'last_name': 'Last name: ',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        """
        Checks that the email is unique.
        If the email already exists in the database, it raises a ValidationError.
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email

    def save(self, commit=True):
        """
        Saves the form data to a User object and generates an activation token.
        It calls the superclass save method to save the form data to a User object,
        but it doesn't save the User object to the database yet.
        It generates a random string for the activation token and saves it to the User object.
        Finally, it saves the User object to the database and returns the User object.
        """
        user = super().save(commit=False)
        user.activation_token = get_random_string(length=32)
        user.save()
        return user


class SimpleRegisterUserForm(RegisterUserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        del self.fields['first_name']
        del self.fields['last_name']

    def clean_email(self):
        """
        Checks that the email is unique.
        If the email already exists in the database, it raises a ValidationError.
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email


class ProfileUserForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Confirm password",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CustomPasswordResetForm(PasswordResetForm):
    # Generates new temporary password
    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False, token_generator=None,
             from_email=None, request=None, extra_email_context=None,
             subject=None, message=None, html_email_template_name=None, **kwargs):

        email = self.cleaned_data["email"]
        user_model = get_user_model()
        try:
            user = user_model._default_manager.get(email=email)
        except user_model.DoesNotExist:
            # Handles the case when the user is not found
            return

        # Generates temporary password
        temp_password = get_random_string(length=12)
        user.set_password(temp_password)
        user.save()

        # Defines the URL for login page
        login_url = reverse('users:login')
        full_login_url = '{}://{}{}'.format('https' if use_https else 'http', domain_override or request.get_host(),
                                            login_url)

        # Sends letter with a temporary password
        subject = 'Your temporary password'
        message = format_html(
            "You're receiving this email because you requested a password reset for your user account at Mail Mate.<br><br>"
            "Your temporary password: {}.<br>"
            "Please use it to login and go to your profile to set your new password.<br><br>"
            "<a href='{}'>Login to Mail Mate</a>",
            temp_password,
            full_login_url
        )
        send_mail(subject, message, from_email, [email], fail_silently=False, html_message=message)

        # Returns None, since Django's tokenization mechanism to reset the password isn't used
        return
