from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from main.models import MailCampaign, Client


class Command(BaseCommand):
    """
        Custom management command to launch a campaign.

       You can run this command from the command line as follows:
              python manage.py launch_campaign <campaign_id>

       Bear in mind that argument (<campaign_id>) must be an integer.

           """
    help = "Launches mail campaign by ID."

    # Adds arguments to the command.
    def add_arguments(self, parser):
        # 'campaign_id' - argument name to use on the command line.
        # Provide a value for this argument when invoking the command.
        parser.add_argument('campaign_id', type=int, help='ID of the MailCampaign to launch')

    def handle(self, *args, **options):
        # options is a dictionary that contains all arguments passed to the command from the command line.
        campaign_id = options['campaign_id']
        try:
            # Gets campaign by id
            campaign = MailCampaign.objects.get(pk=campaign_id)

            # Checks that the campaign has a template and a client_tag
            if campaign.template and campaign.client_tag:
                subj = campaign.template.subject
                msg = campaign.template.body

                clients = Client.objects.filter(tag=campaign.client_tag.tag)
                recipient_list = [client.email for client in clients]

                for recipient in recipient_list:
                    send_mail(
                        subject=subj,
                        message=msg,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient]
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully launched campaign {campaign_id}'))
            else:
                # Handling the case when a template or client tag is missing
                self.stdout.write(self.style.WARNING('Campaign has no template or client tag'))
        except MailCampaign.DoesNotExist:
            self.stdout.write(self.style.ERROR('Campaign does not exist'))
