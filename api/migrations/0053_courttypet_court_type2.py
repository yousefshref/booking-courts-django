# Generated by Django 5.0.2 on 2024-02-26 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_remove_court_type_court_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtTypeT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='court',
            name='type2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.courttypet'),
        ),
    ]
