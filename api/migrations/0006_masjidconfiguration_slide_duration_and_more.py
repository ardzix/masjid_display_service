# Generated by Django 5.1.4 on 2025-03-12 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_midight_prayertime_midnight'),
    ]

    operations = [
        migrations.AddField(
            model_name='masjidconfiguration',
            name='slide_duration',
            field=models.PositiveIntegerField(default=5000),
        ),
        migrations.AddField(
            model_name='masjidconfiguration',
            name='slide_scroll_duration',
            field=models.PositiveIntegerField(default=7000),
        ),
        migrations.AddField(
            model_name='masjidconfiguration',
            name='theme',
            field=models.CharField(choices=[('green', 'Green'), ('red', 'Red'), ('blue', 'Blue'), ('yellow', 'Yellow')], default='green', max_length=10),
        ),
        migrations.AddField(
            model_name='masjidconfiguration',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
