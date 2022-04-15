from django.contrib import admin
from .models import Invoice


class InvoiceModelAdmin(admin.ModelAdmin):
    list_display = ['invoicing_party', 'invoiced_party', 'description', 'created_date']


admin.site.register(Invoice, InvoiceModelAdmin)
