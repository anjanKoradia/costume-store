from validator import Validator


class ProductDetailsValidator(Validator):
    name = "required"
    category = "required"
    rating = "required|digits"
    price = "required|digits"
    discount = "required|digits"
    stock = "required|digits"
    description = "required"

    message = {
        "name": {
            "required": ("Product name is required"),
        },
        "category": {"required": ("Category required")},
        "rating": {
            "required": ("Rating required"),
            "digits": ("Rating must be a positive integer"),
        },
        "price": {
            "required": ("Price required"),
            "digits": ("Price must be a positive integer"),
        },
        "discount": {
            "required": ("Discount required"),
            "digits": ("Discount must be a positive integer"),
        },
        "stock": {
            "required": ("Stock required"),
            "digits": {"Stock must be a positive integer"},
        },
        "description": {"required": ("Description required")},
    }
