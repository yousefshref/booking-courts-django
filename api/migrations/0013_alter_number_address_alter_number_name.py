# Generated by Django 5.0.2 on 2024-04-06 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_number_address_number_image_number_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='number',
            name='name',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
