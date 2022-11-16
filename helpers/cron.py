# helpers.cron.py

import logging
from django.core import management


logger = logging.getLogger(__name__)


def create_backups_scheduled_job():
    try:
        management.call_command("dbbackup")
    except management.DoesNotExist:
        logger.error("The management does not exist with that ID")
