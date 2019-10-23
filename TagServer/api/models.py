from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.models import CustomUser

TAG_METHOD = [
    ("singleMode", "singleMode"),
    ("batchMode", "batchMode")
]

TYPE = [
    ("text", "text"),
    ("image", "image"),
    ("video", "video")
]

STATUS = [
    ("available", "available"),
    ("blocked", "blocked")
]


class Process(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    tag_method = models.CharField(max_length=20, choices=TAG_METHOD, default="singleMode")
    status = models.CharField(max_length=20, choices=STATUS, default="available")
    is_tagged = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Profile(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
    is_multi_content = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class Content(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.TextField(blank=True, null=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE, blank=False, null=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True, related_name='tags')
    title = models.CharField(max_length=100, blank=True, null=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserOutput(models.Model):
    process_id = models.IntegerField(null=False, blank=False)
    profile_id = models.IntegerField(null=False, blank=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "output %d"%self.pk


class OutputTag(models.Model):
    user_output = models.ForeignKey(UserOutput, related_name="tags", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.title
