# Generated by Django 2.0.13 on 2019-11-02 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20191031_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='profiles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pf_tags', to='api.Profile'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='process',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pc_tags', to='api.Process'),
        ),
    ]
