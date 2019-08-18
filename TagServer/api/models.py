from django.contrib.auth.models import AbstractUser
from django.db import models

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
    ("blocked", "blocked"),
    ("tagged", "tagged")
]


class Process(models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    number_of_profiles = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    tagging_method = models.CharField(max_length=20, choices=TAG_METHOD)

    def __str__(self):
        return self.title


class ProfilePackage(models.Model):
    id = models.IntegerField(primary_key=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    has_next = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    packageProfile = models.ForeignKey(ProfilePackage, on_delete=models.CASCADE)
    is_multi_content = models.BooleanField(default=False)
    is_tagged = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS, default="available")
    expire_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return str(self.id)


class Content(models.Model):
    id = models.IntegerField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.TextField(blank=True, null=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE, blank=False, null=False)

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class UserOutput(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    process_id = models.IntegerField(null=False, blank=False)
    profile_id = models.IntegerField(null=False, blank=False)
    tag_title = models.CharField(max_length=100, blank=False, null=False)

