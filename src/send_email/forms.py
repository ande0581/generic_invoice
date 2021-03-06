from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SendEmailForm(forms.Form):

    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'Send Email', css_class='btn=primary'))