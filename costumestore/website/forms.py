from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    """
    A form for adding or updating a cart item.

    This form is used to create or update a cart item with the specified size, color, and quantity.
    It performs validation on the quantity field to ensure it is greater than 0.

    Methods:
        - __init__(self, *args, **kwargs): Initializes the form instance and customizes error messages for fields.
        - clean_quantity(self): Validates the quantity field to ensure it is greater than 0.
    """

    class Meta:
        model = CartItem
        fields = ("size", "color", "quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["size"].error_messages = {
            "required": "Please select valid size.",
        }
        self.fields["color"].error_messages = {
            "required": "Please select valid color.",
        }

    def clean_quantity(self):
        """
        Validates the quantity field.

        Raises:
            - forms.ValidationError: If the quantity is less than or equal to 0.

        Returns:
            - int: The validated quantity value.
        """

        quantity = self.cleaned_data.get("quantity")

        if int(quantity) <= 0:
            raise forms.ValidationError("Quantity must be grater than 0.")

        return quantity
