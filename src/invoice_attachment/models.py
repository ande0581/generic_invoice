from django.db import models
from django.urls import reverse


def generate_filename(instance, filename):

    customer = instance.invoice.invoiced_party.__str__().replace(' ', '_').lower()
    folder = "{}_{}".format(customer, instance.invoice.id)
    url = "customers/{}/{}".format(folder, filename)

    return url


class Document(models.Model):

    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    filename = models.FileField(upload_to=generate_filename)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice.id})

    def __str__(self):
        return self.description

    def shorten_filename(self):
        folder1, folder2, filename = self.filename.name.split('/')
        return filename
