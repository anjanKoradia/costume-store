from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django import forms
import re


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def password_validator(password):
    regx = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$"
    match_regx = re.compile(regx)

    if not match_regx.match(password):
        raise forms.ValidationError(
            "Password must contain at least one uppercase letter, one lowercase letter, one number and one special character."
        )
