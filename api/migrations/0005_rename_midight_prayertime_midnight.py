# Generated by Django 5.1.4 on 2025-02-20 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_prayertime_imsak_prayertime_midight_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prayertime',
            old_name='midight',
            new_name='midnight',
        ),
    ]
