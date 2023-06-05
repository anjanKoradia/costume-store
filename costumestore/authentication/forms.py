from .validator import password_validator
from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, validators=[password_validator]
    )
    cpassword = forms.CharField(
        widget=forms.PasswordInput, required=True, validators=[password_validator]
    )
    role = forms.CharField(required=True)

    def clean_cpassword(self):
        cpassword = self.cleaned_data.get("cpassword")
        password = self.cleaned_data.get("password")

        if cpassword != password:
            raise forms.ValidationError("Passwords do not match.")
        return cpassword
