# Generated by Django 2.2.4 on 2019-08-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190814_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='status',
            field=models.CharField(choices=[('available', 'available'), ('blocked', 'blocked'), ('tagged', 'tagged')], default='available', max_length=20),
        ),
    ]