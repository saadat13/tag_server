# Generated by Django 2.2.4 on 2019-08-28 05:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_auto_20190826_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
