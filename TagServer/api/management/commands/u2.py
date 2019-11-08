import os

from django.core.management.base import BaseCommand, CommandError


import sys
# calculate stuff
import logging

from django.utils import timezone
from django.utils.timezone import make_aware

from api.models import Profile

from api.models import Process


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for i in range(50):
                obj = Profile.objects.create(pk=i+1)
                obj.process = Process.objects.get(pk=3)
                obj.save()
            self.stdout.write("ok!")
        except Exception as e:
            self.stdout.write(str(e))
