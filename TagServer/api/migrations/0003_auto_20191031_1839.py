# Generated by Django 2.0.13 on 2019-10-31 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_useroutput_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_tagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='process',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Process'),
        ),
    ]
