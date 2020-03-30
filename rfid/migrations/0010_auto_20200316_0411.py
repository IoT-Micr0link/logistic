# Generated by Django 3.0.3 on 2020-03-16 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0009_auto_20200313_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='sku',
            name='codigo_SAP',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='descripcion',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='modelo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='ni_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='plataforma_fuente_unidad',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sku',
            name='reference_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='sku',
            name='tipo_unidad',
            field=models.CharField(max_length=200, null=True),
        ),
    ]