from django.contrib import admin
from .models import EmailLog


class EmailLogModelAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'to_address', 'subject', 'body', 'successful', 'invoice', 'invoice_attachment']


admin.site.register(EmailLog, EmailLogModelAdmin)
