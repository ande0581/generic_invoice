from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Sum, Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import InvoiceForm
from .models import Invoice

Customer = apps.get_model('customer', 'Customer')
Document = apps.get_model('invoice_attachment', 'Document')
EmailLog = apps.get_model('send_email', 'EmailLog')
InvoiceItem = apps.get_model('invoice_item', 'InvoiceItem')
PDFImage = apps.get_model('pdf', 'PDFImage')


# Create your views here.
class InvoiceCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'invoice/invoice_form.html'
    form_class = InvoiceForm
    success_message = "Invoice Successfully Added"
    
    def form_valid(self, form):
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
        context['saved_invoices'] = PDFImage.objects.filter(invoice=invoice_obj).order_by('-created_date')
        context['attachments'] = Document.objects.filter(invoice=invoice_obj)
        context['email_log'] = EmailLog.objects.filter(invoice=invoice_obj).order_by('-timestamp')
        invoicing_items_total = invoicing_items_obj.aggregate(Sum('cost'))['cost__sum']
        invoiced_items_total = invoiced_items_obj.aggregate(Sum('cost'))['cost__sum']
        context['invoicing_items_total'] = invoicing_items_total
        context['invoiced_items_total'] = invoiced_items_total

        if invoicing_items_total:
            context['invoicing_items_total_half'] = invoicing_items_total / 2
        else:
            context['invoicing_items_total_half'] = 0

        if invoiced_items_total:
            context['invoiced_items_total_half'] = invoiced_items_total / 2
        else:
            context['invoiced_items_total_half'] = 0

        if invoiced_items_total and invoicing_items_total:

            if invoicing_items_total > invoiced_items_total:
                context['the_owing_party'] = f"{invoice_obj.invoiced_party.first_name} Owes"
                context['the_owing_total'] = (invoicing_items_total / 2) - (invoiced_items_total / 2)
            elif invoicing_items_total < invoiced_items_total:
                context['the_owing_party'] = f"{invoice_obj.invoicing_party.first_name} Owes"
                context['the_owing_total'] = (invoiced_items_total / 2) - (invoicing_items_total / 2)
            elif invoicing_items_total == invoiced_items_total:
                context['the_owing_party'] = "Nobody Owes"
                context['the_owing_total'] = 0
            else:
                raise NotImplemented
        elif invoicing_items_total and not invoiced_items_total:
            context['the_owing_party'] = f"{invoice_obj.invoiced_party.first_name} Owes"
            context['the_owing_total'] = (invoicing_items_total / 2)
        elif invoiced_items_total and not invoicing_items_total:
            context['the_owing_party'] = f"{invoice_obj.invoicing_party.first_name} Owes"
            context['the_owing_total'] = (invoiced_items_total / 2)
        else:
            context['the_owing_party'] = ""
            context['the_owing_total'] = 0

        return context


class InvoiceList(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 20

    def get_queryset(self):
        queryset_list = Invoice.objects.order_by('-id')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(invoiced_party__first_name__icontains=query) |
                Q(invoiced_party__last_name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset_list


