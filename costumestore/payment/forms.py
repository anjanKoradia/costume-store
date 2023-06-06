from django import forms

class BillingDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)
    country = forms.CharField(max_length=50, required=True)
    pin_code = forms.CharField(max_length=10, required=True)
    phone = forms.CharField(max_length=10, required=True)
    email = forms.EmailField(required=True)
    order_note = forms.CharField(required=False)