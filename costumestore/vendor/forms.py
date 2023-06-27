from django import forms
from .models import Product


class ProductDetails(forms.ModelForm):
    """
    A form for creating or updating product details.

    This form is used to capture and validate information related to a product's details,
    such as its name, colors, dimensions, category, subcategory, rating, price, discount,
    stock availability, and description.

    Attributes:
        model (django.db.models.Model): The model class that the form is based on.
        fields (tuple): A tuple of field names to include in the form.

    """

    class Meta:
        model = Product
        fields = (
            "name",
            "colors",
            "dimension",
            "category",
            "subcategory",
            "rating",
            "price",
            "discount",
            "stock",
            "description",
        )
