# Generated by Django 5.0.1 on 2024-02-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_court_offer_from_court_offer_price_per_hour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='location',
            field=models.URLField(null=True),
        ),
    ]
