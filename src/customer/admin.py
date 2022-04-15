from django.contrib import admin
from .models import Customer


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'telephone', 'street', 'city', 'state', 'zip', 'created_date']


admin.site.register(Customer, CustomerModelAdmin)
