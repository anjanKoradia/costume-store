from django import forms
from .models import Product


class ProductDetails(forms.ModelForm):
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
