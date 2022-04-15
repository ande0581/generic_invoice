from django.contrib import admin
from .models import PDFImage


class PDFImageModelAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'filename', 'created_date']


admin.site.register(PDFImage, PDFImageModelAdmin)
