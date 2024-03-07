# Generated by Django 5.0.2 on 2024-03-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_notification_is_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='event',
        ),
        migrations.RemoveField(
            model_name='book',
            name='is_cancelled',
        ),
        migrations.RemoveField(
            model_name='book',
            name='is_paied',
        ),
        migrations.RemoveField(
            model_name='book',
            name='paied',
        ),
        migrations.RemoveField(
            model_name='book',
            name='with_ball',
        ),
        migrations.AddField(
            model_name='booktime',
            name='event',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booktime',
            name='is_cancelled',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='booktime',
            name='is_paied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='booktime',
            name='paied',
            field=models.CharField(blank=True, choices=[('E_Wallet', 'E_Wallet'), ('Cash', 'Cash')], max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='booktime',
            name='with_ball',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booktime',
            name='book_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booktime',
            name='book_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
