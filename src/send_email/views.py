from django.apps import apps
from decouple import config
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic.edit import FormView
import datetime

from .models import EmailLog

Document = apps.get_model('invoice_attachment', 'Document')
Invoice = apps.get_model('invoice', 'Invoice')
PDFImage = apps.get_model('pdf', 'PDFImage')


def generate_filename(instance):
    name = instance.invoiced_party.__str__().replace(' ', '_').lower()
    filename = "{}_{}.pdf".format(name, datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))

    return filename


def log_email(**kwargs):
    invoice_obj = Invoice.objects.get(pk=kwargs['invoice_id'])

    email_entry = EmailLog()
    email_entry.to_address = kwargs['to_address']
    email_entry.subject = kwargs['subject']
    email_entry.body = kwargs['body']
    email_entry.successful = kwargs['successful']
    email_entry.invoice = invoice_obj
    email_entry.invoice_attachment = kwargs['invoice_attachment']
    email_entry.save()


def send_email(pdf_id, to_address, subject, body, attachments):
    pdf_obj = PDFImage.objects.get(pk=pdf_id)
    from_address = config('EMAIL_HOST_USER')
    email = EmailMessage(subject, body, from_address, [to_address])

    # Attach PDF
    email.attach_file(pdf_obj.filename.path)

    # Add any additional attachments selected on form submission
    for attachment in attachments:
        email.attach_file(attachment.filename.path)

    # Attempt to send email
    try:
        response = email.send()
    except Exception:
        response = 0

    # invoice attachment filename
    folder1, folder2, pdf_filename = str(pdf_obj.filename).split('/')

    # Log email in DB
    email_log_entry = {
        'to_address': to_address,
        'subject': subject,
        'body': body,
        'successful': response,
        'invoice_id': pdf_obj.invoice.id,
        'invoice_attachment': pdf_filename
    }

    log_email(**email_log_entry)

    return response


class InvoiceEmailCreate(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'send_email/send_email_form.html'

    def get_initial(self):
        initial = super().get_initial()
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        email_subject = f"{pdf_obj.invoice.invoiced_party.first_name} Invoice #{pdf_obj.invoice.id:04} - {pdf_obj.invoice.description}"
        initial['subject'] = email_subject
        initial['body'] = f"{pdf_obj.invoice.invoiced_party.first_name},\n\nPlease see the attached invoice and let me know if you have any questions.\n\nThanks,\n\n{pdf_obj.invoice.invoicing_party.first_name}"
        return initial

    def get_success_url(self):
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        return reverse('invoice_app:invoice_detail', kwargs={'pk': pdf_obj.invoice.id})

    def form_valid(self, form):
        body = form.cleaned_data['body']
        pdf_obj = PDFImage.objects.get(pk=self.kwargs['pdf_id'])
        attachments = Document.objects.filter(invoice=pdf_obj.invoice.id)
        to_address = pdf_obj.invoice.invoiced_party.email
        subject = form.cleaned_data['subject']
        email_response = send_email(pdf_id=self.kwargs['pdf_id'], to_address=to_address, subject=subject, body=body,
                                    attachments=attachments)
        if email_response:
            messages.success(self.request, 'Successfully sent email to {}'.format(to_address))
        else:
            messages.error(self.request, 'Failed to send email to {}'.format(to_address))
        return super(InvoiceEmailCreate, self).form_valid(form)