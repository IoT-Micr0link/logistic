# Generated by Django 3.0.3 on 2020-03-30 18:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0023_auto_20200330_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreport',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]