# Generated by Django 3.0.3 on 2020-05-09 03:36

import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.CharField(blank=True, max_length=140, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.CharField(blank=True, max_length=140, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Location')),
            ],
        ),
        migrations.CreateModel(
            name='PackingUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('serial_number', models.CharField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReaderAntenna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('serial_number', models.CharField(max_length=140, unique=True)),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rfid.Reader')),
            ],
        ),
        migrations.CreateModel(
            name='ReaderBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=200)),
                ('reference_image', models.ImageField(null=True, upload_to='')),
                ('datasheet', models.FileField(blank=True, null=True, upload_to='')),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransferOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_completion_date', models.DateField(blank=True, null=True)),
                ('actual_completion_date', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('RE', 'Solicitado'), ('IP', 'En Alistamiento'), ('IT', 'En Tránsito'), ('CO', 'Entregado')], default='RE', max_length=3)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Location')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_entries', to='rfid.Location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Location')),
            ],
        ),
        migrations.CreateModel(
            name='TransferOrderTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_reading', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rfid.TransferOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('epc', models.CharField(max_length=150)),
                ('timestamp_reading', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Salida'), ('READ', 'Lectura')], default='READ', max_length=10)),
                ('antenna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.ReaderAntenna')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Node')),
                ('reader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.Reader')),
            ],
        ),
        migrations.AddField(
            model_name='reader',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.ReaderBrand'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('epc', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('last_seen_timestamp', models.DateTimeField(null=True)),
                ('last_seen_action', models.CharField(choices=[('IN', 'Entrada'), ('OUT', 'Salida'), ('READ', 'Lectura')], default='IN', max_length=10)),
                ('display_name', models.CharField(max_length=200)),
                ('data', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('in_transit', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('current_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='current_items', to='rfid.Location')),
                ('last_seen_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.Location')),
                ('packing_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.PackingUnit')),
                ('sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.SKU')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
                ('wait_minutes', models.PositiveIntegerField(default=10)),
                ('all_locations', models.BooleanField(default=False)),
                ('all_skus', models.BooleanField(default=False)),
                ('end_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_end', to='rfid.Location')),
                ('end_sku', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_end', to='rfid.SKU')),
                ('init_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_init', to='rfid.Location')),
                ('init_sku', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inv_request_init', to='rfid.SKU')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryReportLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('cant', models.IntegerField()),
                ('packing_unit', models.CharField(max_length=200)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rfid.InventoryReport')),
            ],
        ),
        migrations.AddField(
            model_name='inventoryreport',
            name='inventory_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='rfid.InventoryRequest'),
        ),
        migrations.AddField(
            model_name='inventoryreport',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rfid.Location'),
        ),
        migrations.CreateModel(
            name='WarehouseEntryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.WarehouseEntry')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Item')),
            ],
            options={
                'unique_together': {('entry', 'item')},
            },
        ),
        migrations.CreateModel(
            name='TransferOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('RE', 'Por alistar'), ('AL', 'Alistado'), ('NOE', 'No entregado'), ('EN', 'Entregado')], default='RE', max_length=3)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Item')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rfid.TransferOrder')),
            ],
            options={
                'unique_together': {('order', 'item')},
            },
        ),
    ]
