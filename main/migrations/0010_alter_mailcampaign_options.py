# Generated by Django 4.2.7 on 2024-01-23 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_mailinglog_campaign_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailcampaign',
            options={'ordering': ['pk'], 'verbose_name': 'mail campaign', 'verbose_name_plural': 'mail campaigns'},
        ),
    ]
