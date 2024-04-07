# Generated by Django 5.0.2 on 2024-04-07 01:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_customuser_x_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courtadditionaltool',
            name='court_additional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tools_court', to='api.courtadditional'),
        ),
    ]