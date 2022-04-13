from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Sum, Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import InvoiceForm
# from address.models import Address
# from generic_invoice_item.models import GenericInvoiceItem
from .models import Invoice
# from send_email.models import EmailLog

from django.apps import apps
Customer = apps.get_model('customer', 'Customer')
InvoiceItem = apps.get_model('invoice_item', 'InvoiceItem')


# Create your views here.
class InvoiceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'invoice/invoice_form.html'
    form_class = InvoiceForm
    success_message = "Invoice Successfully Added"
    
    def form_valid(self, form):
        print('homer', self.kwargs)
        form.instance.customer = Customer.objects.get(pk=self.kwargs['customer'])
        return super(InvoiceCreate, self).form_valid(form)


class InvoiceUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    success_message = "Invoice Successfully Updated"


class InvoiceDelete(LoginRequiredMixin, DeleteView):
    model = Invoice

    def get_object(self, queryset=None):
        obj = super(InvoiceDelete, self).get_object()
        self.invoiced_party_pk = obj.invoiced_party.id
        return obj

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_detail', kwargs={'pk': self.invoiced_party_pk})


class InvoiceDetail(LoginRequiredMixin, DetailView):
    model = Invoice

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetail, self).get_context_data(**kwargs)
        invoice_obj = Invoice.objects.get(pk=self.kwargs['pk'])
        invoicing_items_obj = InvoiceItem.objects.filter(is_invoicing_party=True, invoice=invoice_obj)
        invoiced_items_obj = InvoiceItem.objects.filter(is_invoicing_party=False, invoice=invoice_obj)
        context['invoiced_party'] = Customer.objects.get(id=invoice_obj.invoiced_party.id)
        context['invoicing_party'] = Customer.objects.get(id=invoice_obj.invoicing_party.id)
        context['invoicing_items'] = invoicing_items_obj
        context['invoiced_items'] = invoiced_items_obj
        context['invoicing_items_total'] = invoicing_items_obj.aggregate(Sum('cost'))['cost__sum']
        context['invoiced_items_total'] = invoiced_items_obj.aggregate(Sum('cost'))['cost__sum']
        # context['invoicing_party_total'] = invoice_obj
        # context['generic_invoice_pk'] = self.kwargs['pk']
        # # context['emails'] = EmailLog.objects.filter(customer_id=self.kwargs['pk'])
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(BidDetail, self).get_context_data(**kwargs)
    #     bid_obj = Bid.objects.get(id=self.kwargs['pk'])
    #     bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])


class InvoiceList(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 20

    def get_queryset(self):
        queryset_list = Invoice.objects.order_by('created_date')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(customer__first_name__icontains=query) |
                Q(customer__last_name__icontains=query) |
                Q(customer__company_name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset_list


