# Generated by Django 3.0.3 on 2020-03-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0013_auto_20200316_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='action',
            field=models.CharField(choices=[('IN', 'Entry'), ('OUT', 'Out'), ('READ', 'Reading')], default='READ', max_length=10),
        ),
    ]