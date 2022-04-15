from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import InvoiceItem


class InvoiceItemForm(forms.ModelForm):

    class Meta:
        model = InvoiceItem
        fields = ('description', 'cost', 'split_percentage')

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Save Item', css_class='btn=primary'))
