# Generated by Django 5.2.1 on 2025-05-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='currency',
            field=models.CharField(choices=[('BTC', 'BTC'), ('XRP', 'XRP'), ('USDT', 'USDT'), ('TRX ', 'TRX '), ('LTC ', 'LTC '), ('ETH ', 'ETH '), ('BNB', 'BNB')], default='BTC', max_length=10),
        ),
    ]
