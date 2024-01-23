# Generated by Django 4.2.7 on 2024-01-23 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_mailcampaign_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingmessage',
            options={'ordering': ['pk'], 'verbose_name': 'template', 'verbose_name_plural': 'templates'},
        ),
        migrations.AlterField(
            model_name='mailcampaign',
            name='template',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.mailingmessage'),
            preserve_default=False,
        ),
    ]
