# Generated by Django 3.1.7 on 2021-03-27 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20210327_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.buyer'),
        ),
    ]