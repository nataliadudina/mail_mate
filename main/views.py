from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseNotAllowed
from django.core.exceptions import PermissionDenied
from .models import MailingMessage, Client, MailCampaign, MailingLog
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .forms import TemplateForm, ClientForm, MailCampaignForm
from users.forms import SimpleRegisterUserForm
from django.urls import reverse
from main.jobs import launch_campaign
from main.services import schedule
from django.views.decorators.http import require_POST
from users.services import send_activation_email
from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin


# Denies user access to other objects
class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return self.object


def index(request):
    random_articles = Article.objects.all().order_by('?')[:3]  # Retrieves 3 random articles
    total_campaigns = MailCampaign.objects.all().count()
    active_campaigns = MailCampaign.objects.filter(status='launched').count()
    total_clients = Client.objects.values('email').distinct().count()
    # flat=True means that the values will be represented as a one-dimensional list (not tuples)
    unique_tags_count = Client.objects.values_list('tag', flat=True).distinct().count()

    if request.method == 'POST':
        form = SimpleRegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_activation_email(request, user)
            return redirect('users:activation_sent')
    else:
        form = SimpleRegisterUserForm()

    context = {
        'title': 'Welcome to Mail Mate',
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_clients': total_clients,
        'unique_tags_count': unique_tags_count,
        'random_articles': random_articles,
    }
    return render(request, 'main/index.html', context)


class TemplateListView(LoginRequiredMixin, OwnerRequiredMixin, ListView):
    template_name = 'main/template_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Templates', 'title': 'Templates'}

    def get_queryset(self):
        return MailingMessage.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_messages'] = context['object_list']
        return context


class TemplateCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = MailingMessage
    form_class = TemplateForm
    template_name = 'main/template_form.html'
    extra_context = {'page_title': 'Template', 'title': 'New Template'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        owner = self.request.user
        new_template = form.save(commit=False)
        new_template.owner = owner
        new_template.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('template_edit', kwargs={'pk': self.object.pk})


class TemplateUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = TemplateForm
    template_name = 'main/template_form.html'
    extra_context = {'page_title': 'Template'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        owner = self.request.user
        new_template = form.save(commit=False)
        new_template.owner = owner
        new_template.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('template_edit', kwargs={'pk': self.object.pk})


class TemplateDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = MailingMessage
    template_name = 'main/template_form.html'

    def get_success_url(self):
        return reverse('template_list')


class ClientListView(LoginRequiredMixin, OwnerRequiredMixin, ListView):
    template_name = 'main/client_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Clients', 'title': 'Clients'}

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = context['object_list']
        return context


class ClientCreateView(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    extra_context = {'page_title': 'Client', 'title': 'New Client'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        owner = self.request.user
        new_client = form.save(commit=False)
        new_client.owner = owner
        new_client.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_list')


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    extra_context = {'page_title': 'Client', 'title': 'Edit Client Data'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        owner = self.request.user
        new_client = form.save(commit=False)
        new_client.owner = owner
        new_client.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_list')


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Client
    template_name = 'main/client_form.html'

    def get_success_url(self):
        return reverse('client_list')


class MailCampaignList(LoginRequiredMixin, ListView):
    template_name = 'main/campaign_list.html'
    model = MailCampaign
    paginate_by = 10
    extra_context = {'page_title': 'Campaigns', 'title': 'Campaigns'}

    def is_manager(self):
        return self.request.user.is_manager()

    def get_queryset(self):
        user = self.request.user
        if self.is_manager():
            return MailCampaign.objects.all()
        else:
            return MailCampaign.objects.filter(owner=user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaigns'] = context['object_list']
        return context


class MailCampaignCreate(LoginRequiredMixin, OwnerRequiredMixin, CreateView):
    model = MailCampaign
    form_class = MailCampaignForm
    template_name = 'main/campaign_form.html'
    extra_context = {'page_title': 'Campaign', 'title': 'New Campaign'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        owner = self.request.user
        campaign = form.save(commit=False)
        campaign.owner = owner
        campaign.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MailCampaignCreate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('campaign_list')


class MailCampaignUpdate(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = MailCampaign
    form_class = MailCampaignForm
    template_name = 'main/campaign_form.html'
    extra_context = {'page_title': 'Campaign', 'title': 'Edit Campaign'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        if self.object.status in ('completed', 'launched'):
            self.object.status = 'created'
            self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MailCampaignUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('campaign_list')


class MailCampaignDelete(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = MailCampaign
    template_name = 'main/campaign_form.html'

    def get_success_url(self):
        return reverse('campaign_list')


@require_POST
def start_campaign(request, pk):
    campaign = get_object_or_404(MailCampaign, pk=pk)
    user_email = request.user.email
    launch_campaign(campaign.pk, user_email)  # Run one campaign manually
    return redirect('campaign_list')


@require_POST
def start_all_campaigns(request):
    user_email = request.user.email
    if request.method == 'POST':
        schedule(user_email)  # Run scheduler for all campaigns
        return redirect('campaign_list')
    else:
        return HttpResponseNotAllowed(['POST'])


class MailingLogView(LoginRequiredMixin, OwnerRequiredMixin, ListView):
    model = MailingLog
    template_name = 'main/mailing_logs.html'
    paginate_by = 10
    extra_context = {'page_title': 'Mailing Logs', 'title': 'Mailing Logs'}

    def get_queryset(self):
        return MailingLog.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = context['object_list']
        return context


class ClearLogsView(View):
    def post(self, request):
        MailingLog.objects.filter(owner=self.request.user).delete()
        return redirect('campaign_list')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')
