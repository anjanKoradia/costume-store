from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from validator import Validator


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


class CustomerSignupValidator(Validator):
    name = "required"
    password = "required|password:high"
    confirm_pass = "same:password"

    message = {
        "name": {
            "required": ("Name is required"),
        },
        "password": {
            "required": ("Password is required"),
            "password": (
                "7 characters or longer. Combine upper and lower case letters, special characters and digit."
            ),
        },
        "confirm_pass": {"same": ("Password dose not matched")},
    }
