# Generated by Django 3.0.3 on 2020-03-27 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0016_auto_20200326_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='epc',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reading',
            name='epc',
            field=models.CharField(max_length=150),
        ),
    ]
