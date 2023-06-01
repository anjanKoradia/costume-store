from django import forms
from .models import Address


class VendorProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    shop_name = forms.CharField(max_length=100)
    aadhar_number = forms.CharField(max_length=12, min_length=12)
    aadhar_image = forms.FileField()
    pancard_number = forms.CharField(max_length=10, min_length=10)
    pancard_image = forms.FileField()
    gst_number = forms.CharField(max_length=15, min_length=15)
    business_license = forms.FileField()
    

class VendorProfileForm_Name_Only(forms.Form):
    name = forms.CharField(max_length=100)
    shop_name = forms.CharField(max_length=100)
    

class VendorAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("address", "pin_code", "city", "state", "country")