# Generated by Django 5.0.1 on 2024-02-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_alter_booksetting_book_overtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktime',
            name='book_to_date_cancel',
            field=models.DateField(blank=True, null=True),
        ),
    ]
