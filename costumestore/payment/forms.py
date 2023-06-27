from django import forms


class BillingDetailsForm(forms.Form):
    """
    A form for capturing billing details.

    This form is used to collect customer billing information such as name, address,
    city, state, country, pin code, phone number, email, and an optional order note.

    Attributes:
    - name (CharField): The name of the customer (maximum length: 100 characters).
    - address (CharField): The customer's address.
    - city (CharField): The city of the customer's address (maximum length: 50 characters).
    - state (CharField): The state of the customer's address (maximum length: 50 characters).
    - country (CharField): The country of the customer's address (maximum length: 50 characters).
    - pin_code (CharField): The PIN code or postal code of the customer's address (maximum length: 10 characters).
    - phone (CharField): The phone number of the customer (maximum length: 10 characters).
    - email (EmailField): The email address of the customer.
    - order_note (CharField, optional): An optional note or additional information about the order.

    """

    name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(required=True)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)
    country = forms.CharField(max_length=50, required=True)
    pin_code = forms.CharField(max_length=10, required=True)
    phone = forms.CharField(max_length=10, required=True)
    email = forms.EmailField(required=True)
    order_note = forms.CharField(required=False)
