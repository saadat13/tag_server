# Generated by Django 2.2.4 on 2019-08-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_process_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='status',
            field=models.CharField(choices=[(1, 'available'), (2, 'blocked'), (3, 'tagged')], default='available', max_length=20),
        ),
    ]
