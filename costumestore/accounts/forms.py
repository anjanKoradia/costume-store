from django import forms
from .models import Address


class VendorProfileForm(forms.Form):
    """
    A form for creating or updating a vendor profile.

    This form includes fields for the vendor's personal and business information,
    such as name, shop name,Aadhar number, Aadhar image, PAN card number, PAN card
    image, GST number, and business license.

    Fields:
    - name (CharField): The name of the vendor (max length: 100).
    - shop_name (CharField): The name of the vendor's shop (max length: 100).
    - aadhar_number (CharField): The vendor's Aadhar number (exact length: 12).
    - aadhar_image (FileField): An image file of the vendor's Aadhar card.
    - pancard_number (CharField): The vendor's PAN card number (exact length: 10).
    - pancard_image (FileField): An image file of the vendor's PAN card.
    - gst_number (CharField): The vendor's GST number (exact length: 15).
    - business_license (FileField): An image file of the vendor's business license.
    """

    name = forms.CharField(max_length=100)
    shop_name = forms.CharField(max_length=100)
    aadhar_number = forms.CharField(max_length=12, min_length=12)
    aadhar_image = forms.FileField()
    pancard_number = forms.CharField(max_length=10, min_length=10)
    pancard_image = forms.FileField()
    gst_number = forms.CharField(max_length=15, min_length=15)
    business_license = forms.FileField()


class VendorProfileFormNameOnly(forms.Form):
    """
    A form for updating the name and shop name of a vendor profile.

    This form includes fields for the vendor's name and shop name.

    Fields:
    - name (CharField): The name of the vendor (max length: 100).
    - shop_name (CharField): The name of the vendor's shop (max length: 100).
    """

    name = forms.CharField(max_length=100)
    shop_name = forms.CharField(max_length=100)


class VendorAddressForm(forms.ModelForm):
    """
    A form for creating or updating a vendor's address.

    This form is based on the Address model and includes fields for the address,
    pin code, city, state, and country.

    Model:
    - Address: The model representing a vendor's address.

    Fields:
    - address (CharField): The vendor's address.
    - pin_code (CharField): The pin code of the vendor's location.
    - city (CharField): The city of the vendor's location.
    - state (CharField): The state of the vendor's location.
    - country (CharField): The country of the vendor's location.
    """

    class Meta:
        model = Address
        fields = ("address", "pin_code", "city", "state", "country")
