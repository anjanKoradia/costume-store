import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django import forms


def is_valid_email(email):
    """
    Check if an email address is valid.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def password_validator(password):
    """
    Validate a password using a regular expression pattern.

    The password must contain at least one uppercase letter, one lowercase letter,
    one number, and one special character. The length of the password should be
    between 8 and 15 characters.

    Args:
        password (str): The password to be validated.

    Raises:
        forms.ValidationError: If the password does not meet the validation criteria.
    """
    regx = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$"
    match_regx = re.compile(regx)

    if not match_regx.match(password):
        raise forms.ValidationError(
            '''Password must contain at least one uppercase letter, one lowercase 
            letter,one number and one special character.'''
        )
