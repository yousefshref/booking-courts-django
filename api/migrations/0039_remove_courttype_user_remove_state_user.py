# Generated by Django 5.0.1 on 2024-02-23 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_courttype_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courttype',
            name='user',
        ),
        migrations.RemoveField(
            model_name='state',
            name='user',
        ),
    ]
