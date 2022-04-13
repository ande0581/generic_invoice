from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView
from django.views.generic import ListView

from .pdf_template import generate_pdf
from .models import PDFImage
# from bid.models import Bid
# from bid_item.models import BidItem
from django.apps import apps
Invoice = apps.get_model('invoice', 'Invoice')
InvoiceItem = apps.get_model('invoice_item', 'InvoiceItem')


# def create_bid_item_dict(bid_obj):
#     """
#     :param bid_obj:
#     :return: dictionary where the key is the job_type and the value is biditem_obj that matches that job_type
#     """
#     bid_item_obj = BidItem.objects.filter(bid=bid_obj.id)
#
#     unique_job_types = set()
#     for item in bid_item_obj:
#         unique_job_types.add(item.job_type)
#
#     bid_item_dict = {}
#     for job in unique_job_types:
#         bid_items = bid_item_obj.filter(job_type=job)
#         bid_item_dict.setdefault(job, bid_items)
#
#     return bid_item_dict


@login_required()
def view_pdf(request, return_file_object=False, **kwargs):
    obj = Invoice.objects.get(pk=kwargs['invoice_id'])
    #invoice_item_dict = create_bid_item_dict(obj)
    #invoice_item_dict = InvoiceItem.objects.get(invoice=obj)
    invoice_item_dict = None
    # response = generate_pdf(request, obj=obj, bid_item_dict=bid_item_dict, invoice=invoice, employee=employee,
    #                         save_to_disk=False, return_file_object=return_file_object)
    response = generate_pdf(request, obj=obj, invoice_item_dict=invoice_item_dict, save_to_disk=False)
    return response


@login_required()
def save_pdf(request, **kwargs):
    obj = Invoice.objects.get(pk=kwargs['invoice_id'])
    invoice_item_dict = None
    # bid_item_dict = create_bid_item_dict(obj)
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

