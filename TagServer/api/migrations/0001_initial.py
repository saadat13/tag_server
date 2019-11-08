# Generated by Django 2.0.13 on 2019-10-24 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(blank=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(choices=[('text', 'text'), ('image', 'image'), ('video', 'video')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OutputTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('tag_method', models.CharField(choices=[('singleMode', 'singleMode'), ('batchMode', 'batchMode')], default='singleMode', max_length=20)),
                ('status', models.CharField(choices=[('available', 'available'), ('blocked', 'blocked')], default='available', max_length=20)),
                ('is_tagged', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=False)),
                ('expert_user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experts', to=settings.AUTH_USER_MODEL)),
                ('full_expert_user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fulls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_multi_content', models.BooleanField(default=False)),
                ('process', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.Process')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('process', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.Process')),
            ],
        ),
        migrations.CreateModel(
            name='UserOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_id', models.IntegerField()),
                ('profile_id', models.IntegerField()),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='outputtag',
            name='user_output',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.UserOutput'),
        ),
        migrations.AddField(
            model_name='content',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Profile'),
        ),
    ]