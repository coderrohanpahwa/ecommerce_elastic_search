# Generated by Django 3.1.7 on 2021-03-30 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20210330_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='seller',
            field=models.OneToOneField(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.seller'),
        ),
        migrations.DeleteModel(
            name='AvailabilityPerSeller',
        ),
    ]
