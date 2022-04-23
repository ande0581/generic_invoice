from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic import ListView

from .pdf_template import generate_pdf
from .models import PDFImage

Customer = apps.get_model('customer', 'Customer')
Invoice = apps.get_model('invoice', 'Invoice')
InvoiceItem = apps.get_model('invoice_item', 'InvoiceItem')

# TODO clean-up pdf.views


def create_invoice_item_dict(invoice_obj):
    invoicing_items_obj = InvoiceItem.objects.filter(is_invoicing_party=True, invoice=invoice_obj)
    invoiced_items_obj = InvoiceItem.objects.filter(is_invoicing_party=False, invoice=invoice_obj)

    # total cost of toms items
    invoicing_items_total = invoicing_items_obj.aggregate(Sum('cost'))['cost__sum']

    # total cost of saras items
    invoiced_items_total = invoiced_items_obj.aggregate(Sum('cost'))['cost__sum']

    # total amount that tom paid
    tom_paid_total = invoicing_items_obj.aggregate(Sum('invoicing_party_cost'))['invoicing_party_cost__sum']

    # total amount that sara paid
    sara_paid_total = invoiced_items_obj.aggregate(Sum('invoiced_party_cost'))['invoiced_party_cost__sum']

    # total amount tom owes
    what_tom_owes = invoiced_items_obj.aggregate(Sum('invoicing_party_cost'))['invoicing_party_cost__sum']

    # total amount sara owes
    what_sara_owes = invoicing_items_obj.aggregate(Sum('invoiced_party_cost'))['invoiced_party_cost__sum']

    if not what_tom_owes:
        what_tom_owes = 0

    if not what_sara_owes:
        what_sara_owes = 0

    if what_tom_owes > what_sara_owes:
        the_owing_party = f"{invoice_obj.invoicing_party.first_name} Owes"
        the_owing_total = what_tom_owes - what_sara_owes
    elif what_sara_owes > what_tom_owes:
        the_owing_party = f"{invoice_obj.invoiced_party.first_name} Owes"
        the_owing_total = what_sara_owes - what_tom_owes
    elif what_tom_owes == what_sara_owes:
        the_owing_party = "Nobody Owes"
        the_owing_total = 0
    else:
        raise NotImplemented

    invoice_items_dict = {
        'invoicing_items_obj': invoicing_items_obj,
        'invoiced_items_obj': invoiced_items_obj,
        'invoicing_items_total': invoicing_items_total,
        'invoiced_items_total': invoiced_items_total,
        'tom_paid_total': tom_paid_total,
        'sara_paid_total': sara_paid_total,
        'what_tom_owes': what_tom_owes,
        'what_sara_owes': what_sara_owes,
        'the_owing_party': the_owing_party,
        'the_owing_total': the_owing_total
    }

    return invoice_items_dict


@login_required()
def view_pdf(request, return_file_object=False, **kwargs):
    obj = Invoice.objects.get(pk=kwargs['invoice_id'])
    invoice_item_dict = create_invoice_item_dict(invoice_obj=obj)
    # response = generate_pdf(request, obj=obj, bid_item_dict=bid_item_dict, invoice=invoice, employee=employee,
    #                         save_to_disk=False, return_file_object=return_file_object)
    response = generate_pdf(request, obj=obj, invoice_item_dict=invoice_item_dict, save_to_disk=False)
    return response


@login_required()
def save_pdf(request, **kwargs):
    obj = Invoice.objects.get(pk=kwargs['invoice_id'])
    invoice_item_dict = create_invoice_item_dict(invoice_obj=obj)
    # response = generate_pdf(request, obj=obj, bid_item_dict=bid_item_dict, invoice=invoice, employee=employee,
    #                         save_to_disk=True)
    response = generate_pdf(request, obj=obj, invoice_item_dict=invoice_item_dict, save_to_disk=True)
    return response


class PDFImageList(LoginRequiredMixin, ListView):
    model = PDFImage

    def get_context_data(self, **kwargs):
        context = super(PDFImageList, self).get_context_data(**kwargs)
        context['object_list'] = PDFImage.objects.filter(invoice=self.kwargs['pk']).order_by('-created_date')
        context['invoice_id'] = self.kwargs['pk']
        return context


class PDFImageDelete(LoginRequiredMixin, DeleteView):
    model = PDFImage

    def get_object(self, queryset=None):
        obj = super(PDFImageDelete, self).get_object()
        self.invoice_pk = obj.invoice.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('invoice_app:invoice_detail', kwargs={'pk': self.invoice_pk})

