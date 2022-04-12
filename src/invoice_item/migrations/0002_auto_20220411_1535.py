# Generated by Django 3.2.12 on 2022-04-11 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('invoice', '0005_auto_20220411_1416'),
        ('invoice_item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoicedPartyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('cost', models.FloatField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
            ],
            options={
                'verbose_name_plural': 'InvoicingPartyItems',
            },
        ),
        migrations.CreateModel(
            name='InvoicingPartyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('cost', models.FloatField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
            ],
            options={
                'verbose_name_plural': 'InvoicingPartyItems',
            },
        ),
        migrations.DeleteModel(
            name='InvoiceItem',
        ),
    ]
