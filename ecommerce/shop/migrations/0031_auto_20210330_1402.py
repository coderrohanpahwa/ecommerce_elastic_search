# Generated by Django 3.1.7 on 2021-03-30 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_availability_per_seller'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Availability_per_seller',
            new_name='AvailabilityPerSeller',
        ),
    ]
