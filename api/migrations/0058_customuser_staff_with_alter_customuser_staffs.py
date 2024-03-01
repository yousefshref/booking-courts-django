# Generated by Django 5.0.2 on 2024-02-28 09:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_alter_customuser_staffs'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='staff_with',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='staffs',
            field=models.ManyToManyField(blank=True, null=True, related_name='all_staffs', to=settings.AUTH_USER_MODEL),
        ),
    ]
