from django.contrib import admin
from .models import  Process,ProfilePackage , Profile, Content, Tag, UserOutput

# Register your models here.
admin.site.register(Process)
admin.site.register(ProfilePackage)
admin.site.register(Profile)
admin.site.register(Content)
admin.site.register(Tag)
admin.site.register(UserOutput)

