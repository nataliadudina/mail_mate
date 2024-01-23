from django import forms
from .models import MailingMessage, Client, MailCampaign
from django.forms.widgets import DateTimeInput


class TemplateForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ['name', 'subject', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Template name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'cols': 65, 'rows': 15, 'placeholder': 'Content'})
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment', 'tag']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'comment': forms.Textarea(attrs={'cols': 60, 'rows': 5, 'placeholder': 'Comment'}),
            'tag': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tag'}),
        }


class MailCampaignForm(forms.ModelForm):
    class Meta:
        model = MailCampaign
        fields = ['campaign_name', 'send_time', 'frequency', 'template', 'client_tag']
        widgets = {
            'campaign_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Campaign name'}),
            'send_time': DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super(MailCampaignForm, self).__init__(*args, **kwargs)
        self.fields['client_tag'].queryset = Client.objects.order_by('tag').distinct('tag')
