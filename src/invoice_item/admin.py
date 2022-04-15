from django.contrib import admin
from .models import InvoiceItem


class InvoiceItemModelAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'is_invoicing_party', 'description', 'cost', 'split_percentage', 'invoicing_party_cost',
                    'invoiced_party_cost']


admin.site.register(InvoiceItem, InvoiceItemModelAdmin)
