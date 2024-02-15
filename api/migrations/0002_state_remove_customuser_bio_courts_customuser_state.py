# Generated by Django 5.0.1 on 2024-02-14 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.CreateModel(
            name='Courts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155, null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('open', models.TimeField(null=True)),
                ('close', models.TimeField(null=True)),
                ('with_ball', models.BooleanField(default=True, null=True)),
                ('ball_price', models.IntegerField(blank=True, null=True)),
                ('event', models.BooleanField(default=False, null=True)),
                ('event_price', models.IntegerField(blank=True, null=True)),
                ('event_from', models.TimeField(blank=True, null=True)),
                ('event_to', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.state')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.state'),
        ),
    ]
