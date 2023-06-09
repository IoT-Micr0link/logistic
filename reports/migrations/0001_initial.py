# Generated by Django 4.0 on 2023-02-20 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
                ('wait_minutes', models.PositiveIntegerField(default=10)),
                ('all_locations', models.BooleanField(default=False)),
                ('all_skus', models.BooleanField(default=False)),
                ('end_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_end', to='inventory.location')),
                ('end_sku', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_end', to='inventory.sku')),
                ('init_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_init', to='inventory.location')),
                ('init_sku', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_init', to='inventory.sku')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryReportLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('cant', models.IntegerField()),
                ('packing_unit', models.CharField(max_length=200)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.inventoryreport')),
            ],
        ),
        migrations.AddField(
            model_name='inventoryreport',
            name='inventory_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='reports.inventoryrequest'),
        ),
        migrations.AddField(
            model_name='inventoryreport',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.location'),
        ),
    ]
