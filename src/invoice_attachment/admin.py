from django.contrib import admin
from .models import Document


class DocumentModelAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'description', 'filename', 'uploaded_date']


admin.site.register(Document, DocumentModelAdmin)
