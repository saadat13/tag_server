import os

from django.core.management.base import BaseCommand, CommandError
from api.models import Profile

import sys
# calculate stuff
import logging

from django.utils import timezone
from django.utils.timezone import make_aware



class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Profile.objects\
                .filter(status="blocked", expire_date__lte=timezone.now())\
                .update(status="available", expire_date=None)
            self.stdout.write("ok!")
        except Exception as e:
            self.stdout.write(str(e))
