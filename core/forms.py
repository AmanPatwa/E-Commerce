from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

payment_choices = {
    ('C','Credit Card'),
    ('D','Debit Card'),
    ('P','Paypal')
}

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget = forms.TextInput(attrs = {
        'placeholder':'1234 Main St',
        'class':'form-control'
    }))
    appartment_address = forms.CharField(widget = forms.TextInput(attrs = {
        'placeholder':'Apartment or suite',
        'class':'form-control'
    }),required = False)
    country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs = {
        'class':'custom-select d-block w-100'
    }))
    zip = forms.CharField(widget = forms.TextInput(attrs = {
        'class':'form-control'
    }))
    address_required  = forms.BooleanField(widget = forms.CheckboxInput() , required=False)
    save_info  = forms.BooleanField(widget = forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget = forms.RadioSelect, choices=payment_choices)