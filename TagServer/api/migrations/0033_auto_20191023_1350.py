# Generated by Django 2.2.4 on 2019-10-23 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0032_auto_20191023_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='user',
        ),
        migrations.AddField(
            model_name='useroutput',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
