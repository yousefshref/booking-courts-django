# Generated by Django 5.0.2 on 2024-04-07 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_courtadditional_court'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
