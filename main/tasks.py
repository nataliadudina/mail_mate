from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from smtplib import SMTPException
from main.models import MailCampaign, Client
from .utils import log_attempt
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)    # creates logger


def launch_campaign(campaign_id):
    print(f"Launching campaign {campaign_id}")
    """
        Retrieves a campaign by ID from the database.
        Checks if the campaign has a template and a client tag.
        Retrieves clients associated with the client tag.
        Constructs an email with the template's subject and body.
        Sends the email to each recipient.
        """

    # Gets campaign by id
    campaign = MailCampaign.objects.get(pk=campaign_id)
    launching = timezone.now()
    print('launch')

    try:
        # Checks that the campaign has a template and a client_tag
        if campaign.template and campaign.client_tag:
            subj = campaign.template.subject
            msg = campaign.template.body

            clients = Client.objects.filter(tag=campaign.client_tag.tag)
            recipient_list = [client.email for client in clients]

            campaign.status = 'launched'
            campaign.save()

            for recipient in recipient_list:
                try:
                    send_mail(
                        subject=subj,
                        message=msg,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient]
                    )

                except BadHeaderError as e:
                    log_attempt(campaign, launching, status='failed', response=f"Bad header error for {recipient}. Error: {e}")
                    continue
                except SMTPException as e:
                    log_attempt(campaign, launching, status='failed', response=f"SMTP error for {recipient}. Error: {e}")
                    continue
                except Exception as e:
                    log_attempt(campaign, launching, status='failed', response=f"Error sending email to {recipient}. Error: {e}")
                    continue

            completing = timezone.now()
            campaign.status = 'completed'
            campaign.save()
            server_response = 'Campaign completed successfully.'
            log_attempt(campaign, launching, status='completed', end_time=completing, response=server_response)
            logger.info(f"Campaign completed successfully.")

        else:
            # Case, when template or client tag is missing
            campaign.status = 'created'
            campaign.save()
            logger.error("Template or client tag is missing for the campaign.")
            log_attempt(campaign, launching, status='failed')
    except Exception as e:
        campaign.status = 'created'
        campaign.save()
        logger.error(f"Error sending email: {e}")
