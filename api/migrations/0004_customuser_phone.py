# Generated by Django 5.0.1 on 2024-02-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_customuser_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
