from cerberus import Validator

ProductDetailsValidator = {
    "name": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "category": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "rating": {
        "type": "float",
        "min": 0,
        "max": 5,
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "price": {
        "type": "integer",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "discount": {
        "type": "integer",
        "min": 0,
        "max": 100,
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "stock": {
        "type": "integer",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "description": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
}


def validate_data(schema, fields):
    v = Validator(schema)
    v.validate(fields)
    errors = v.errors

    return errors
