# Generated by Django 5.0.2 on 2024-02-28 08:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='staff_with',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]