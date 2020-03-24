# Generated by Django 3.0.3 on 2020-03-16 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0012_item_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_entries', to='rfid.Location')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rfid.Location')),
            ],
        ),
        migrations.AddField(
            model_name='sku',
            name='datasheet',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='transferorder',
            name='state',
            field=models.CharField(choices=[('RE', 'Solicitado'), ('IP', 'En progreso'), ('CO', 'Completado')], default='RE', max_length=3),
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
        migrations.RunSQL('create or replace view  inventory_summary as '
                          'select row_number() OVER () as id, sku_id , last_seen_location_id, count(*) '
                          'from rfid_item '
                          'group by sku_id, last_seen_location_id ')
    ]
