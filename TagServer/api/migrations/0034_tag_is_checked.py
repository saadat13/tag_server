# Generated by Django 2.2.4 on 2019-10-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20191023_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='is_checked',
            field=models.BooleanField(default=False),
        ),
    ]
