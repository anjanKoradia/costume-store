from validator import Validator


class ProductDetailsValidator(Validator):
    name = "required"
    category = "required"
    rating = "required|pos_integer"
    price = "required|pos_integer"
    discount = "required|pos_integer"
    stock = "required|pos_integer"
    description = "required"
    images = "required"

    message = {
        "name": {
            "required": ("Product name is required"),
        },
        "category": {"required": ("Category required")},
        "rating": {
            "required": ("Rating required"),
            "pos_integer": ("Rating must be a positive integer"),
        },
        "price": {
            "required": ("Price required"),
            "pos_integer": ("Price must be a positive integer"),
        },
        "discount": {
            "required": ("Discount required"),
            "pos_integer": ("Discount must be a positive integer"),
        },
        "stock": {
            "required": ("Stock required"),
            "pos_integer": {"Stock must be a positive integer"},
        },
        "description": {"required": ("Description required")},
        "images": {"required":{"Image required"}}
    }
