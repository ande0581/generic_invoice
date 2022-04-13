# Generated by Django 3.2.12 on 2022-04-11 11:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, help_text='Enter a brief invoice description', max_length=128)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('cost', models.FloatField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
            ],
            options={
                'verbose_name_plural': 'InvoiceItems',
            },
        ),
    ]