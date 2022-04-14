from django.conf.urls import url
from .views import AttachmentUpload, AttachmentList, AttachmentDelete


app_name = 'invoice_attachment_app'
urlpatterns = [
    url(r'^upload/(?P<invoice_id>\d+)/$', AttachmentUpload.as_view(), name='invoice_attachment_upload'),
    url(r'^list/(?P<invoice_id>\d+)/$', AttachmentList.as_view(), name='invoice_attachment_list'),
    url(r'^delete/(?P<pk>\d+)/$', AttachmentDelete.as_view(), name='invoice_attachment_delete'),
]