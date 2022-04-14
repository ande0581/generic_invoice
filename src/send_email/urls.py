from django.conf.urls import url
from .views import InvoiceEmailCreate
from .forms import SendEmailForm

app_name = 'send_email_app'
urlpatterns = [
    url(r'^(?P<pdf_id>\d+)/$', InvoiceEmailCreate.as_view(form_class=SendEmailForm),
        name='email_create'),
]