# Generated by Django 3.2.12 on 2022-04-15 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_item', '0006_invoiceitem_split_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='invoiced_party_cost',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='invoicing_party_cost',
            field=models.FloatField(null=True),
        ),
    ]
