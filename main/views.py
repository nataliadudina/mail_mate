from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import MailingMessage, Client, MailCampaign, MailingLog
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .forms import TemplateForm, ClientForm, MailCampaignForm
from users.forms import SimpleRegisterUserForm
from django.urls import reverse
from main.tasks import launch_campaign
from django.views.decorators.http import require_POST
from users.services import send_activation_email
from blog.models import Article


def index(request):
    random_articles = Article.objects.all().order_by('?')[:3]  # Retrieves 3 random articles
    total_campaigns = MailCampaign.objects.all().count()
    active_campaigns = MailCampaign.objects.filter(status='created').count()
    total_clients = Client.objects.all().count()
    # flat=True means that the values will be represented as a one-dimensional list (not tuples)
    unique_tags_count = Client.objects.values_list('tag', flat=True).distinct().count()

    if request.method == 'POST':
        form = SimpleRegisterUserForm(request.POST)
        if form.is_valid():
            # Save the data
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


class TemplateListView(ListView):
    template_name = 'main/template_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Templates', 'title': 'Templates'}

    def get_queryset(self):
        return MailingMessage.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_messages'] = context['object_list']
        return context


class TemplateCreateView(CreateView):
    model = MailingMessage
    form_class = TemplateForm
    template_name = 'main/template_form.html'
    extra_context = {'page_title': 'Template', 'title': 'New Template'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('template_edit', kwargs={'pk': self.object.pk})


class TemplateUpdateView(UpdateView):
    model = MailingMessage
    form_class = TemplateForm
    template_name = 'main/template_form.html'
    extra_context = {'page_title': 'Template'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('template_edit', kwargs={'pk': self.object.pk})


class TemplateDeleteView(DeleteView):
    model = MailingMessage
    template_name = 'main/template_form.html'

    def get_success_url(self):
        return reverse('template_list')


class ClientListView(ListView):
    template_name = 'main/client_list.html'
    paginate_by = 10
    extra_context = {'page_title': 'Clients', 'title': 'Clients'}

    def get_queryset(self):
        return Client.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = context['object_list']
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    extra_context = {'page_title': 'Client', 'title': 'New Client'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    extra_context = {'page_title': 'Client', 'title': 'Edit Client Data'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'main/client_form.html'

    def get_success_url(self):
        return reverse('client_list')


# def show_client_tags(request, tag_slug):
#     tag = get_object_or_404(Client, slug=tag_slug)
#     clients = Client.objects.filter()


class MailCampaignList(ListView):
    template_name = 'main/campaign_list.html'
    model = MailCampaign
    paginate_by = 10
    extra_context = {'page_title': 'Campaigns', 'title': 'Campaigns'}

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campaigns'] = context['object_list']
        return context


class MailCampaignCreate(CreateView):
    model = MailCampaign
    form_class = MailCampaignForm
    template_name = 'main/campaign_form.html'
    extra_context = {'page_title': 'Campaign', 'title': 'New Campaign'}

    # Override the form_valid method to handle form submission
    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('campaign_list')


class MailCampaignUpdate(UpdateView):
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

    def get_success_url(self):
        return reverse('campaign_list')


class MailCampaignDelete(DeleteView):
    model = MailCampaign
    template_name = 'main/campaign_form.html'

    def get_success_url(self):
        return reverse('campaign_list')


@require_POST
def start_campaign(request, pk):
    # Runs the campaign when it is launched manually
    campaign = get_object_or_404(MailCampaign, pk=pk)
    launch_campaign(campaign.pk)  # Launches campaign
    return redirect('campaign_list')


class MailingLogView(ListView):
    model = MailingLog
    template_name = 'main/mailing_logs.html'
    paginate_by = 10
    extra_context = {'page_title': 'Mailing Logs', 'title': 'Mailing Logs'}

    def get_queryset(self):
        try:
            # Filtering of mailings by launched and completed statuses
            return MailingLog.objects.all()
        except OperationalError as e:
            return HttpResponseServerError("Database Error: " + str(e))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            mailing_logs = self.get_queryset()
            context['mailing_list'] = mailing_logs
        except OperationalError as e:
            context['mailing_list'] = []
            context['error_message'] = "Database Error: " + str(e)

        return context


class ClearLogsView(View):
    def post(self, request):
        MailingLog.objects.all().delete()
        return redirect('campaign_list')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Oops! This page has not been created yet.</h1>')
