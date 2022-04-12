from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import InvoiceItem
from .forms import InvoiceItemForm

from django.apps import apps
Invoice = apps.get_model('invoice', 'Invoice')


# class BidItemCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     template_name = 'bid_item/biditem_form.html'
#     form_class = BidItemForm
#     success_message = "Successfully Added Item"
#
#     def form_valid(self, form):
#         form.instance.bid = Bid.objects.get(pk=self.kwargs['bid'])
#         form.instance.cost = Service.objects.values_list('cost').filter(description=form.cleaned_data['description'])[0][0]
#         form.instance.total = form.instance.quantity * form.instance.cost
#         return super(BidItemCreate, self).form_valid(form)


class InvoiceItemCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'invoice_item/invoiceitem_form.html'
    form_class = InvoiceItemForm
    success_message = "Successfully Added Item"

    def form_valid(self, form):
        form.instance.invoice = Invoice.objects.get(pk=self.kwargs['invoice'])
        form.instance.is_invoicing_party = self.kwargs['is_invoicing_party']
        return super(InvoiceItemCreate, self).form_valid(form)


class InvoiceItemUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'invoice_item/invoiceitem_form.html'
    model = InvoiceItem
    form_class = InvoiceItemForm
    success_message = "Successfully Updated Item"


class InvoiceItemDelete(LoginRequiredMixin, DeleteView):
    model = InvoiceItem

    def get_object(self, queryset=None):
        obj = super(InvoiceItemDelete, self).get_object()
        self.invoice_pk = obj.invoice.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice_pk})
