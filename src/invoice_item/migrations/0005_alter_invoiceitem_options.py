# Generated by Django 3.2.12 on 2022-04-15 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_item', '0004_alter_invoiceitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoiceitem',
            options={'verbose_name_plural': 'Invoice Items'},
        ),
    ]