from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Invoice


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('invoicing_party', 'invoiced_party', 'description')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Invoice', css_class='btn=primary'))
