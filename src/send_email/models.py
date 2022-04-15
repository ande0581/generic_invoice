from django.db import models
from django.urls import reverse


class EmailLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    to_address = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    successful = models.BooleanField()
    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE)
    invoice_attachment = models.CharField(max_length=100)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice.id})