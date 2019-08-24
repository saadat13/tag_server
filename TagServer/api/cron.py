from .models import Profile
from datetime import datetime, time
import os


def unblock_scheduled_job():
    os.environ['TZ'] = 'Asia/Tehran'
    time.tzset()
    try:
        Profile.objects.filter(status="blocked", expire_date__gte=datetime.now()).update(status="available", expire_date=None)
        return "database updated successfully"
    except Exception as e:
        return str(e)