from django.contrib import admin
from main.models import MailCampaign, MailingLog, MailingMessage, Client


@admin.register(MailCampaign)
class MailCampaignAdmin(admin.ModelAdmin):
    fields = ['campaign_name', 'template', 'client_tag', 'send_time', 'frequency']
    list_display = ['campaign_name', 'template', 'client_tag', 'send_time', 'frequency', 'status']
    list_display_links = ('campaign_name',)
    list_editable = ['frequency']
    readonly_fields = ('status',)
    ordering = ['pk']
    list_filter = ('campaign_name',)
    search_fields = ('campaign_name', 'template__name', 'client_tag__tag',)
    list_per_page = 10
    save_on_top = True
#     list_select_related = ('category',)  # pre-loads related categories


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    fields = ['name', 'subject', 'body']
    list_display = ['pk', 'name', 'subject']
    list_display_links = ('name',)
    list_editable = ['subject']
    list_filter = ('name', 'subject',)
    ordering = ['pk']
    list_per_page = 10
    search_fields = ('name', 'subject',)
    save_on_top = True


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ('email', 'full_name', 'tag', 'comment')
    list_display = ('email', 'full_name', 'tag')
    list_filter = ('email', 'tag', 'full_name',)
    list_display_links = ('email',)
    list_editable = ('tag',)
    ordering = ['tag']
    list_per_page = 10
    save_on_top = True


@admin.register(MailingLog)
class MailingLog(admin.ModelAdmin):
    fields = ('campaign_name', 'attempt_datetime', 'completion_datetime', 'status', 'server_response')
    list_display = ('campaign_name', 'attempt_datetime', 'completion_datetime', 'status',)
    list_filter = ('campaign_name', 'status',)
    list_display_links = ('campaign_name',)
    readonly_fields = ('campaign_name', 'attempt_datetime', 'completion_datetime', 'status', 'server_response')
    ordering = ['campaign_name']
    list_per_page = 10
