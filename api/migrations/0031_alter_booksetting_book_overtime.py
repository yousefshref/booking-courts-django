# Generated by Django 5.0.1 on 2024-02-21 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_book_booksetting_booktime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksetting',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_setting', to='api.book'),
        ),
        migrations.CreateModel(
            name='OverTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_from', models.TimeField(blank=True, null=True)),
                ('book_to', models.TimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_over_time', to='api.book')),
            ],
        ),
    ]
