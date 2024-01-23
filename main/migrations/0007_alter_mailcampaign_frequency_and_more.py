# Generated by Django 4.2.7 on 2024-01-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_mailcampaign_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailcampaign',
            name='frequency',
            field=models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='mailcampaign',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('created', 'Created'), ('launched', 'Launched')], default='created', max_length=10),
        ),
    ]
