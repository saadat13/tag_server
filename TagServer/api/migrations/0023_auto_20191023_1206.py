# Generated by Django 2.2.4 on 2019-10-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20191023_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='tag_method',
            field=models.CharField(choices=[('singleMode', 'singleMode'), ('batchMode', 'batchMode')], default='singleMode', max_length=20),
        ),
    ]
