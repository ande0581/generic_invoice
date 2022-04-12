from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Customer
from .forms import CustomerForm

from django.apps import apps
Invoice = apps.get_model('invoice', 'Invoice')


class CustomerCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'customer/customer_form.html'
    form_class = CustomerForm
    success_message = "Successfully Created: %(first_name)s %(last_name)s"


class CustomerUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_message = "Successfully Updated: %(first_name)s %(last_name)s"


class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer

    def get_success_url(self):
        messages.success(self.request, "Successfully Deleted")
        return reverse('customer_app:customer_list')


class CustomerDetail(LoginRequiredMixin, DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(CustomerDetail, self).get_context_data(**kwargs)
        print('jimmy', self.kwargs)
        context['invoices'] = Invoice.objects.filter(invoiced_party_id=self.kwargs['pk'])
        return context

        # context = super(BidDetail, self).get_context_data(**kwargs)
        # bid_obj = Bid.objects.get(id=self.kwargs['pk'])
        # bid_item_obj = BidItem.objects.filter(bid=self.kwargs['pk'])
        # bid_item_dict = create_bid_item_dict(bid_obj)
        # total_cost = bid_item_obj.aggregate(Sum('total'))['total__sum']
        # payment_obj = Payment.objects.filter(bid=self.kwargs['pk'])
        # total_payments = payment_obj.aggregate(Sum('amount'))['amount__sum']
        #
        # context['bid_item_dict'] = bid_item_dict
        # context['total_cost'] = total_cost
        # context['pdfs'] = PDFImage.objects.all().filter(bid=self.kwargs['pk'])
        # context['journal_entries'] = Journal.objects.all().filter(bid=self.kwargs['pk']).order_by('-timestamp')
        # context['payments'] = Payment.objects.all().filter(bid=self.kwargs['pk']).order_by('date')
        # context['date'] = date.today()
        #
        # if total_payments:
        #     context['remaining_balance'] = total_cost - total_payments
        # else:
        #     context['remaining_balance'] = total_cost
        #
        # return context


class CustomerList(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 20

    def get_queryset(self):
        queryset_list = Customer.objects.order_by('last_name')
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(company_name__icontains=query) |
                Q(telephone__icontains=query) |
                Q(email__icontains=query)
            ).distinct()

        return queryset_list

