from django.db import models
from django.urls import reverse
from django.utils import timezone


class Invoice(models.Model):
    invoicing_party = models.ForeignKey('customer.Customer', related_name='invoicing_party', on_delete=models.CASCADE,
                                        help_text='The party creating the invoice')
    invoiced_party = models.ForeignKey('customer.Customer', related_name='invoiced_party', on_delete=models.CASCADE,
                                       help_text='The party receiving the invoice')
    description = models.CharField(max_length=128, blank=True, help_text="Enter a brief invoice description")
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.id})