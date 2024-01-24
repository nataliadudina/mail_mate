from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.CharField(max_length=100, unique=True, db_index=True)
    content = models.TextField(blank=True, null=True, db_index=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    image = models.ImageField(upload_to='images/blog/', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    publication = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PUBLISHED,
    )
    views_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'

    def get_absolute_url(self):
        return reverse('view', kwargs={'slug': self.slug})
