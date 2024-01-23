from .models import MailingLog


def log_attempt(campaign, start_time, status, end_time=None, response=None):
    campaign_name = campaign.campaign_name

    # Makes notes to MailingLog
    logging = MailingLog(
        mailing=campaign,
        campaign_name=campaign_name,
        attempt_datetime=start_time,
        completion_datetime=end_time,
        status=status,
        server_response=response
    )
    print(logging)
    logging.save()
