# Generated by Django 2.2.4 on 2019-08-14 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('expert', 'Expert'), ('full_expert', 'Full expert')], default='Expert', max_length=20),
        ),
    ]
