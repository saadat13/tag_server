
from django.core.management.base import BaseCommand, CommandError
from api.models import Profile,Process, Content


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            for i in range(50):
                obj = Content.objects.create(pk=i+1)
                obj.url = 'https://picsum.photos/id/' + str(i+1) + '/300/300/'
                obj.title = 'image number ' + str(i+1)
                obj.type = 'image'
                obj.profile = Profile.objects.get(pk=i+1)
                obj.save()
            self.stdout.write("ok!")
        except Exception as e:
            self.stdout.write(str(e))
