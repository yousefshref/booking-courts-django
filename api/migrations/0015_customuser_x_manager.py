# Generated by Django 5.0.2 on 2024-04-06 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_number_address_alter_number_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='x_manager',
            field=models.BooleanField(default=False),
        ),
    ]
