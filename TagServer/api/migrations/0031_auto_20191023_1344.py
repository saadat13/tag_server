# Generated by Django 2.2.4 on 2019-10-23 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20191023_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='process',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.Process'),
        ),
    ]