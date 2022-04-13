# Generated by Django 3.2.12 on 2022-04-11 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('invoice', '0004_auto_20220411_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='payer_1',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='payer_2',
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoiced_party',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invoiced_party', to='customer.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoicing_party',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invoicing_party', to='customer.customer'),
            preserve_default=False,
        ),
    ]