# Generated by Django 5.0.2 on 2024-04-02 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_court_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courttype',
            options={'verbose_name': 'CourtType', 'verbose_name_plural': 'CourtTypes'},
        ),
        migrations.AlterModelOptions(
            name='courttypet',
            options={'verbose_name': 'CourtSize', 'verbose_name_plural': 'CourtSizes'},
        ),
    ]
