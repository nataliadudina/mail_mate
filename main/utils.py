import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import BadHeaderError, send_mail
from smtplib import SMTPException
from main.models import Client, MailingLog


logger = logging.getLogger(__name__)


def send_emails(campaign, user_email):
    subj = campaign.template.subject
    msg = campaign.template.body
    start_time = timezone.now()

    try:
        # Checks that the campaign has a client_tag
        if campaign.client_tag:
            clients = Client.objects.filter(tag=campaign.client_tag.tag)
            recipient_list = [client.email for client in clients]

            for recipient in recipient_list:
                try:
                    send_mail(
                        subject=subj,
                        message=msg,
                        from_email=user_email,
                        recipient_list=[recipient]
                    )

                except (BadHeaderError, SMTPException, Exception) as e:
                    handle_email_error(campaign, recipient, e)
                    continue

            server_response = 'Campaign completed successfully.'
            MailingLog.objects.create(
                owner=campaign.owner,
                mailing=campaign,
                campaign_name=campaign.campaign_name,
                attempt_datetime=start_time,
                status='completed',
                completion_datetime=timezone.now(),
                server_response=server_response
            )

        else:
            # Case, when client tag is missing
            campaign.status = 'created'
            campaign.save()
            server_response = 'Template or client tag is missing for the campaign.'
            logger.error("Template or client tag is missing for the campaign.")

            MailingLog.objects.create(
                owner=campaign.owner,
                mailing=campaign,
                campaign_name=campaign.campaign_name,
                attempt_datetime=start_time,
                status='failed',
                server_response=server_response
            )
    except Exception as e:
        campaign.status = 'created'
        campaign.save()
        logger.error(f"An error occurred during email sending: {e}")
        server_response = f"An error occurred during email sending: {e}"
        MailingLog.objects.create(
            owner=campaign.owner,
            mailing=campaign,
            campaign_name=campaign.campaign_name,
            attempt_datetime=start_time,
            status='failed',
            server_response=server_response
        )


def handle_email_error(campaign, recipient, error):
    logger.error(f"Error sending email to {recipient}. Error: {error}")


def update_campaign_status(campaign):
    if campaign.frequency == 'not set':
        campaign.status = 'completed'
    else:
        campaign.status = 'launched'
        frequency_delta = {'daily': timedelta(days=1),
                           'weekly': timedelta(weeks=1),
                           'monthly': timedelta(days=30)}
        campaign.send_time += frequency_delta.get(campaign.frequency, timedelta(days=1))

    campaign.save()
    logger.info('Campaign completed successfully.')


def handle_campaign_error(campaign, error):
    campaign.status = 'created'
    campaign.save()
    logger.error(f"Error launching campaign: {error}")
