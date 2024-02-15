# Generated by Django 5.0.1 on 2024-02-14 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_court_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='court',
            name='location',
        ),
        migrations.AddField(
            model_name='court',
            name='lang',
            field=models.CharField(max_length=355, null=True),
        ),
        migrations.AddField(
            model_name='court',
            name='lat',
            field=models.CharField(max_length=355, null=True),
        ),
    ]
