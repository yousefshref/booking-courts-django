# Generated by Django 5.0.1 on 2024-02-16 12:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_book_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourtAdditional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.court')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourtAdditionalTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('court_additional', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.courtadditional')),
            ],
        ),
    ]