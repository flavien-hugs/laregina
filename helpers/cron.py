# helpers.cron.py

from django.core import management


def create_backups_scheduled_job():
    try:
        management.call_command('dbbackup')
    except:
        pass
