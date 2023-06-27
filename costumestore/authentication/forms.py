from django import forms
from .validator import password_validator


class RegistrationForm(forms.Form):
    """
    A form for user registration.

    This form includes fields for email, name, password, confirm password, and role.
    It performs validation to ensure that the passwords match.

    Attributes:
        email (forms.EmailField): Field for user's email address.
        name (forms.CharField): Field for user's name.
        password (forms.CharField): Field for user's password.
        cpassword (forms.CharField): Field for confirming user's password.
        role (forms.CharField): Field for user's role.
    """

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
        """
        Validates the confirm password field.

        This method compares the value of the confirm password field (cpassword) with
        the password field and raises a ValidationError if they do not match.

        Returns:
            str: The value of the confirm password field (cpassword) if it matches the password field.

        Raises:
            forms.ValidationError: If the confirm password field does not match the password field.
        """
        cpassword = self.cleaned_data.get("cpassword")
        password = self.cleaned_data.get("password")

        if cpassword != password:
            raise forms.ValidationError("Passwords do not match.")
        return cpassword
