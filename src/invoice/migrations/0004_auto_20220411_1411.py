# Generated by Django 3.2.12 on 2022-04-11 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('invoice', '0003_delete_invoiceitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='customer',
        ),
        migrations.AddField(
            model_name='invoice',
            name='payer_1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='primary_payer', to='customer.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='payer_2',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_payer', to='customer.customer'),
            preserve_default=False,
        ),
    ]
