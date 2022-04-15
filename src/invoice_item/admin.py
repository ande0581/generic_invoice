from django.contrib import admin
from .models import InvoiceItem


class InvoiceItemModelAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'is_invoicing_party', 'description', 'cost']


admin.site.register(InvoiceItem, InvoiceItemModelAdmin)
