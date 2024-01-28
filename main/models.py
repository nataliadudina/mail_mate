from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Client(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField()
    full_name = models.CharField(max_length=255, verbose_name='Full Name')
    comment = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.tag}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ['tag']
        unique_together = (('owner', 'email'),)


class MailingMessage(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(verbose_name='Content')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'template'
        verbose_name_plural = 'templates'
        ordering = ['pk']


class MailCampaign(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=100)
    send_time = models.DateTimeField(blank=True, null=True)

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=10, blank=True, null=True, choices=FREQUENCY_CHOICES)

    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('created', 'Created'),
        ('launched', 'Launched'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    template = models.ForeignKey(MailingMessage, on_delete=models.CASCADE)
    client_tag = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        # Django creates method get_<field_name>_display() when choices are used
        return f'{self.campaign_name} - {self.client_tag} - {self.get_status_display()}'

    def formatted_send_time(self):
        # Returns 'not set' if field send_time is not set
        return timezone.localtime(self.send_time).strftime("%d.%m.%Y - %H:%M") if self.send_time else "not set"

    def save(self, *args, **kwargs):
        if self.frequency is None:
            self.frequency = 'not set'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'mail campaign'
        verbose_name_plural = 'mail campaigns'
        ordering = ['pk']


class MailingLog(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    mailing = models.ForeignKey(MailCampaign, on_delete=models.CASCADE, related_name='mailing')
    campaign_name = models.CharField(max_length=100)
    attempt_datetime = models.DateTimeField()
    completion_datetime = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('launched', 'Launched'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.campaign_name} - {self.attempt_datetime} - {self.status}'

    class Meta:
        verbose_name = 'mailing log'
        verbose_name_plural = 'mailing logs'
        ordering = ['attempt_datetime']
