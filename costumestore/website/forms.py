from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ("size", "color", "quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['size'].error_messages = {
            'required': 'Please select valid size.',
        }
        self.fields['color'].error_messages = {
            'required': 'Please select valid color.',
        }
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        
        if int(quantity) <= 0:
            raise forms.ValidationError("Quantity must be grater than 0.")
        
        return quantity