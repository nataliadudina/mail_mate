import logging
from django.conf import settings
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from main.models import MailCampaign
from main.jobs import launch_campaign


logger = logging.getLogger(__name__)


def check_and_filter_campaigns(user_email):
    try:
        campaigns = MailCampaign.objects.filter(status__in=['created', 'launched'], send_time__lte=timezone.now())

        # List for storing IDs of campaigns to be launched
        campaigns_to_launch = []

        for campaign in campaigns:
            if campaign.status == 'created':
                campaign.status = 'launched'
                campaigns_to_launch.append(campaign.id)

        # Status updates for campaigns
        MailCampaign.objects.filter(id__in=campaigns_to_launch).update(status='launched')

        # Runs campaigns
        for campaign_id in campaigns_to_launch:
            launch_campaign(campaign_id, user_email)

    except Exception as e:
        logger.exception("Error occurred while checking and filtering campaigns: %s", e)


def schedule(user_email, *args, **options):
    """
    Checks and schedules campaigns that are in 'created' or 'launched' status and have a specified send_time.
    Iterates through all filtered campaigns and schedules the campaign for immediate launch or at the specified send_time
    using the APScheduler.
    If the campaign's send_time is less than or equal to the current time, the campaign is launched immediately.
    Otherwise, the campaign is scheduled for launch at the specified send_time.
    """
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        check_and_filter_campaigns,
        args=[user_email],
        trigger=CronTrigger(minute="*/1"),
        id="check_campaigns_job",
        max_instances=1,
        replace_existing=True
    )

    try:
        scheduler.start()
        logger.info("Starting scheduler...")
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")
