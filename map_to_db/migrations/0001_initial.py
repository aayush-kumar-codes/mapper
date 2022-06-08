# Generated by Django 3.2 on 2022-06-07 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyModel',
            fields=[
                ('currency', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='MappingModel',
            fields=[
                ('id', models.UUIDField(default='', primary_key=True, serialize=False)),
                ('depo', models.DecimalField(blank=True, decimal_places=8, max_digits=11)),
                ('vol_offset', models.DecimalField(blank=True, decimal_places=8, max_digits=11)),
                ('FTX_feed_ticker', models.CharField(blank=True, max_length=50)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map_to_db.currencymodel')),
            ],
            options={
                'verbose_name_plural': 'Mapped Data',
            },
        ),
    ]
