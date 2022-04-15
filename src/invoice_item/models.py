from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse


class InvoiceItem(models.Model):

    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE)
    is_invoicing_party = models.BooleanField(null=False)
    description = models.CharField(max_length=100)
    cost = models.FloatField(null=True)
    invoicing_party_cost = models.FloatField(null=True)
    invoiced_party_cost = models.FloatField(null=True)
    split_percentage = models.IntegerField(default=50, help_text="This is the percentage the invoicing party (Tom) is going to pay towards the total cost")

    class Meta:
        verbose_name_plural = 'Invoice Items'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice.id})


def invoiceitem_model_pre_save_receiver(sender, instance, *args, **kwargs):
    invoiced_party_percentage = 100 - instance.split_percentage
    invoicing_party_percentage = 100 - invoiced_party_percentage

    instance.invoicing_party_cost = instance.cost * (invoicing_party_percentage/100)
    instance.invoiced_party_cost = instance.cost * (invoiced_party_percentage/100)


pre_save.connect(invoiceitem_model_pre_save_receiver, sender=InvoiceItem)
