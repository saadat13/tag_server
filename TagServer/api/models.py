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
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    number_of_profiles = models.IntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    tagging_method = models.CharField(max_length=20, choices=TAG_METHOD)
    users = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.title


class ProfilePackage(models.Model):
    id = models.IntegerField(primary_key=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)  # process which this package is related to
    has_next = models.BooleanField(default=False)   # defines whether this package has next or not
    status = models.CharField(max_length=20, choices=STATUS, default="available")  # defines whether package is available or blocked by users
    expire_date = models.CharField(max_length=50, null=True, blank=True)  # defines how much time user has to tag profiles of this package
    is_valid = models.BooleanField(default=False)   # defines whether this package is validated by full expert or not
    is_tagged = models.BooleanField(default=False)  # defines whether this package is already tagged by users or not

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    packageProfile = models.ForeignKey(ProfilePackage, on_delete=models.CASCADE)
    is_multi_content = models.BooleanField(default=False)

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
    percent = models.PositiveIntegerField(default=0, null=True, blank=True)
    users = models.ManyToManyField(CustomUser, blank=True)

    def __str__(self):
        return self.title


class UserOutput(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    process_id = models.IntegerField(null=False, blank=False, default=0)
    profile_package_id = models.IntegerField(null=False, blank=False, default=0)
    profile_id = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return "output %d"%self.id


class OutputTag(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    user_output = models.ForeignKey(UserOutput, related_name="tags", on_delete=models.CASCADE)
    tag_title = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tag_title
