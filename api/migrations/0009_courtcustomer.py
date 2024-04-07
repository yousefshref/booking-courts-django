# Generated by Django 5.0.2 on 2024-04-06 15:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('court', 'user')},
            },
        ),
    ]
