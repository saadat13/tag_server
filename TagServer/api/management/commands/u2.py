import os

from django.core.management.base import BaseCommand, CommandError
from api.models import ProfilePackage

import sys
# calculate stuff
import logging

from django.utils import timezone
from django.utils.timezone import make_aware



class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            ProfilePackage.objects\
                .filter(status="blocked")\
                .update(status="available")
            self.stdout.write("ok!")
        except Exception as e:
            self.stdout.write(str(e))
