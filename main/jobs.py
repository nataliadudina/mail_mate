from main.models import MailCampaign
from main.utils import send_emails, update_campaign_status, handle_campaign_error


def launch_campaign(campaign_id, user_email):
    """
        Retrieves a campaign by ID from the database.
        Checks if the campaign has a client tag.
        Retrieves clients associated with the client tag.
        Constructs an email with the template's subject and body.
        Sends the email to each recipient.
        """
    campaign = MailCampaign.objects.get(pk=campaign_id)

    try:
        send_emails(campaign, user_email)
        update_campaign_status(campaign)
    except Exception as e:
        handle_campaign_error(campaign, e)
