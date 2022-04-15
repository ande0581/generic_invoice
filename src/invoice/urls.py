from django.conf.urls import url
from .views import InvoiceCreate, InvoiceDelete, InvoiceUpdate, InvoiceDetail


app_name = 'invoice_app'
urlpatterns = [
    url(r'^(?P<pk>\d+)/$', InvoiceDetail.as_view(), name='invoice_detail'),
    url(r'^(?P<pk>\d+)/update/$', InvoiceUpdate.as_view(), name='invoice_update'),
    url(r'^create/(?P<customer>\d+)/$', InvoiceCreate.as_view(), name='invoice_create'),
    url(r'^(?P<pk>\d+)/delete/$', InvoiceDelete.as_view(), name='invoice_delete'),
]