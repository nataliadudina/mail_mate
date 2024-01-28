from django.urls import path
from .views import TemplateListView, TemplateCreateView, TemplateUpdateView, TemplateDeleteView, ClientListView, \
    ClientCreateView, ClientUpdateView, ClientDeleteView, MailCampaignList, MailCampaignCreate, MailCampaignUpdate, \
    MailCampaignDelete, MailingLogView, ClearLogsView, start_campaign, start_all_campaigns
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('templates/', TemplateListView.as_view(), name='template_list'),
    path('templates/template-form/', TemplateCreateView.as_view(), name='template_form'),
    path('templates/<int:pk>/edit/', TemplateUpdateView.as_view(), name='template_edit'),
    path('templates/<int:pk>/delete/', TemplateDeleteView.as_view(), name='template_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/client-form/', ClientCreateView.as_view(), name='client_form'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('campaigns/', MailCampaignList.as_view(), name='campaign_list'),
    path('campaigns/campaign-form/', MailCampaignCreate.as_view(), name='campaign_form'),
    path('campaigns/<int:pk>/edit/', MailCampaignUpdate.as_view(), name='campaign_edit'),
    path('campaigns/<int:pk>/delete/', MailCampaignDelete.as_view(), name='campaign_delete'),
    path('campaigns/start/<int:pk>/', start_campaign, name='start_campaign'),
    path('campaigns/run-all-campaigns/', start_all_campaigns, name='run_all_campaigns'),

    path('logs/', MailingLogView.as_view(), name='mailing_logs'),
    path('clear_logs/', ClearLogsView.as_view(), name='clear_logs'),
]
