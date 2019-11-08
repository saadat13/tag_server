# Generated by Django 2.0.13 on 2019-10-31 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191031_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='expert_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='process',
            name='full_expert_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fulls', to=settings.AUTH_USER_MODEL),
        ),
    ]