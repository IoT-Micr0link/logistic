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
            name='TransferOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_completion_date', models.DateField()),
                ('actual_completion_date', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('RE', 'Solicitado'), ('IP', 'En Alistamiento'), ('IT', 'En Tránsito'), ('CO', 'Entregado')], default='RE', max_length=3)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.location')),
            ],
            options={
                'db_table': 'transfer_order',
            },
        ),
        migrations.CreateModel(
            name='WarehouseEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_entries', to='inventory.location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.location')),
            ],
            options={
                'db_table': 'warehouse_entry',
            },
        ),
        migrations.CreateModel(
            name='TransferOrderTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_reading', models.DateTimeField(auto_now_add=True)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.transferorder')),
            ],
            options={
                'db_table': 'transfer_order_tracking',
            },
        ),
        migrations.CreateModel(
            name='WarehouseEntryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouseentry')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.item')),
            ],
            options={
                'db_table': 'warehouse_entry_item',
                'unique_together': {('entry', 'item')},
            },
        ),
        migrations.CreateModel(
            name='TransferOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('RE', 'Por alistar'), ('AL', 'Alistado'), ('NOE', 'No entregado'), ('EN', 'Entregado')], default='RE', max_length=3)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='inventory.item')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.transferorder')),
            ],
            options={
                'db_table': 'transfer_order_item',
                'unique_together': {('order', 'item')},
            },
        ),
    ]
