from django import forms
from .models import Product, Color, Size, SIZE_CHOICES

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
    colors = forms.MultipleChoiceField(choices=[])
    sizes = forms.MultipleChoiceField(choices=SIZE_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['colors'].choices = [(color.name, color.name) for color in Color.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        colors = cleaned_data.get('colors')
        sizes = cleaned_data.get('sizes')
        
        if not colors or len(colors) < 1:
            self.errors["colors"] = ["Please select at least one color."]
        
        if not sizes or len(sizes) < 1:
            self.errors["sizes"] = ["Please select at least one size."]
        return cleaned_data
    
    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "subcategory",
            "rating",
            "price",
            "discount",
            "stock",
            "description",
        )

    # def clean_color(self):
    #     breakpoint()
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     colors = cleaned_data.get('colors')
    #     sizes = cleaned_data.get('sizes')
    #     breakpoint()
    #     if not colors:
    #         self.errors["colors"] = ["Please select at least one color."]
        
    #     if not sizes:
    #         self.errors["sizes"] = ["Please select at least one size."]
            
    #     return cleaned_data