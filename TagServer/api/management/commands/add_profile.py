from api.models import Profile, Process

for i in range(50):
    obj = Profile.objects.create()
    obj.process=Process.objects.get(pk=3)