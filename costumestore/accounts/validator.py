from cerberus import Validator

VendorDetailsSchema = {
    "name": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "shop_name": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    }
}

VendorIdentitySchema = {
    "name": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "shop_name": {
        "type": "string",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "aadhar_number": {
        "type": "string",
        "minlength": 12,
        "maxlength": 12,
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "pancard_number": {
        "type": "string",
        "minlength": 10,
        "maxlength": 10,
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "gst_number": {
        "type": "string",
        "minlength": 15,
        "maxlength": 15,
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "aadhar_image": {
        "type": "list",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "pancard_image": {
        "type": "list",
        "required": True,
        "empty": False,
        "nullable": False,
    },
    "business_license": {       
        "type": "list",
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