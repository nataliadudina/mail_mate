from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_image', 'publication', 'time_created',)
    fields = ('title', 'content', 'image', 'show_image', 'publication', 'time_created',)
    list_display_links = ('title',)
    list_editable = ['publication']
    readonly_fields = ('time_created', 'show_image',)
    ordering = ['title']
    list_filter = ('title',)
    search_fields = ('title', 'content')
    actions = ['set_published', 'set_draft']
    list_per_page = 10
    save_on_top = True

# Provides a path if there is an image, otherwise leaves the field empty to avoid exception
    @admin.display(description='Image')
    def show_image(self, post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=80>")
        return ""

    # adds actions to the action drop-down list
    @admin.action(description='Set "published" status')
    def set_published(self, request, queryset):
        count = queryset.update(status=Article.Status.PUBLISHED)
        self.message_user(request, f'The status of {count} items set to "published".')

    @admin.action(description='Set "draft" status')
    def set_draft(self, request, queryset):
        count = queryset.update(status=Article.Status.DRAFT)
        self.message_user(request, f'The status of {count} items set to "draft".', messages.WARNING)
