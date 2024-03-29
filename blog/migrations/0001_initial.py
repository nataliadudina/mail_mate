# Generated by Django 4.2.7 on 2024-01-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', models.CharField(db_index=True, max_length=100, unique=True)),
                ('content', models.TextField(blank=True, db_index=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/blog/')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('publication', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('views_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
        ),
    ]
