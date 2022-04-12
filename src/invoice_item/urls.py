from django.conf.urls import url
from .views import InvoiceItemCreate, InvoiceItemDelete, InvoiceItemUpdate


app_name = 'invoice_item_app'
urlpatterns = [
    url(r'^(?P<pk>\d+)/update/$', InvoiceItemUpdate.as_view(), name='invoice_item_update'),
    url(r'^create/(?P<invoice>\d+)/(?P<is_invoicing_party>\w+)/$', InvoiceItemCreate.as_view(), name='invoice_item_create'),
    url(r'^(?P<pk>\d+)/delete/$', InvoiceItemDelete.as_view(), name='invoice_item_delete'),
]