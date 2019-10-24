from django.contrib import admin
from .models import  Process , Profile, Content, Tag, UserOutput, OutputTag


# Register your models here.
admin.site.register(Process)
admin.site.register(Profile)
admin.site.register(Content)
admin.site.register(Tag)
admin.site.register(UserOutput)
admin.site.register(OutputTag)
