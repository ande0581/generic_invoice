from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import FormView, DeleteView

from .models import Document
from .forms import DocumentForm

Invoice = apps.get_model('invoice', 'Invoice')


class AttachmentList(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'invoice_attachment/invoice_attachment_list.html'

    def get_queryset(self):
        queryset_list = Document.objects.filter(invoice=self.kwargs['invoice_id'])
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(AttachmentList, self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context


class AttachmentUpload(LoginRequiredMixin, FormView):

    template_name = 'invoice_attachment/invoice_attachment_form.html'
    form_class = DocumentForm

    def get_context_data(self, **kwargs):
        context = super(AttachmentUpload, self).get_context_data(**kwargs)
        context['invoice_id'] = self.kwargs['invoice_id']
        return context

    def form_valid(self, form):
        filename = form.cleaned_data['filename']
        description = form.cleaned_data['description']
        invoice_obj = Invoice.objects.get(pk=self.kwargs['invoice_id'])
        Document.objects.create(filename=filename, description=description, invoice=invoice_obj)
        return super(AttachmentUpload, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Document Successfully Uploaded")
        return reverse('invoice_attachment_app:invoice_attachment_list', kwargs={'invoice_id': self.kwargs['invoice_id']})


class AttachmentDelete(LoginRequiredMixin, DeleteView):

    model = Document
    template_name = 'invoice_attachment/invoice_attachment_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(AttachmentDelete, self).get_object()
        self.invoice_pk = obj.invoice.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('invoice_attachment_app:invoice_attachment_list', kwargs={'invoice_id': self.invoice_pk})
