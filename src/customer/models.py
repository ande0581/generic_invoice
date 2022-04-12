from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse


class Customer(models.Model):
    first_name = models.CharField(max_length=64, help_text="Enter the customer's first name")
    last_name = models.CharField(max_length=64, blank=True, help_text="Enter the customer's last name")
    email = models.EmailField(help_text="Enter the customer email address", blank=True)
    telephone = models.CharField(max_length=10, blank=True, help_text="Enter the customer telephone number")
    street = models.CharField(max_length=128, blank=True, help_text="Enter the street address")
    city = models.CharField(max_length=50, blank=True, help_text="Enter the city")
    state = models.CharField(max_length=2, blank=True, help_text="Enter the 2 digit state abbreviation")
    zip = models.CharField(max_length=5, blank=True, help_text="Enter the 5 digit zipcode")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('customer_app:customer_detail', kwargs={'pk': self.pk})


def customer_model_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.email = instance.email.lower()


pre_save.connect(customer_model_pre_save_receiver, sender=Customer)
