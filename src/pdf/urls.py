from django.conf.urls import url
from .views import view_pdf, save_pdf, PDFImageList, PDFImageDelete


app_name = 'pdf_app'
urlpatterns = [
    url(r'^view/(?P<invoice_id>\d+)/invoice/$', view_pdf, name='pdf_view_invoice'),
    url(r'^save/(?P<invoice_id>\d+)/invoice/$', save_pdf, name='pdf_save_invoice'),
    url(r'^list/(?P<pk>\d+)/$', PDFImageList.as_view(), name='pdf_list'),
    url(r'^delete/(?P<pk>\d+)/$', PDFImageDelete.as_view(), name='pdf_delete'),
]