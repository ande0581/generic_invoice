# Generated by Django 3.2.12 on 2022-04-15 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_item', '0005_alter_invoiceitem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='split_percentage',
            field=models.IntegerField(default=50),
        ),
    ]