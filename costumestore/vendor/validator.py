from validator import Validator


class CustomerSignupValidator(Validator):
    name = "required"
    colors = "required"
    password = "required|password:high"
    confirm_pass = "same:password"
    role = "required"

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
        "role": {"required": ("Role is required")},
    }
