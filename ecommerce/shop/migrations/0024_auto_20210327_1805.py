# Generated by Django 3.1.7 on 2021-03-27 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20210327_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shipment'),
        ),
    ]
