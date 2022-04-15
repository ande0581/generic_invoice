from django.db import models
from django.urls import reverse


class InvoiceItem(models.Model):

    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE)
    is_invoicing_party = models.BooleanField(null=False)
    description = models.CharField(max_length=100)
    cost = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = 'Invoice Items'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice.id})