from django.db import models
from common.models import BaseModel


class Address(BaseModel):
    """
    Represents a user address.

    This model stores the information about a user's address, including the 
    address type (billing or default), the address details (text field), 
    pin code, city, state, country, and the associated user.

    Attributes:
        user (ForeignKey): The user associated with the address.
        address (TextField): The address details.
        pin_code (CharField): The pin code of the address.
        city (CharField): The city of the address.
        state (CharField): The state of the address.
        country (CharField): The country of the address.
        type (CharField): The type of the address (choices: 'Billing', 'Default').

    Meta:
        db_table (str): The name of the database table for the Address model.
        verbose_name (str): The human-readable name for a single address object.
        verbose_name_plural (str): The human-readable name for multiple address objects.
    """

    ADDRESS_TYPE = (
        ("Billing", "Billing"),
        ("Default", "Default"),
    )

    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="address"
    )
    address = models.TextField(blank=True)
    pin_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE, default="Default")

    class Meta:
        db_table = "addresses"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Vendor(BaseModel):
    """
    Represents a vendor in the system.

    This model stores information about a vendor, including their 
    user account, shop details, identification documents, verification 
    status, and other related information.

    Attributes:
        user (OneToOneField): The user account associated with the vendor.
        shop_name (CharField): The name of the vendor's shop.
        aadhar_number (CharField): The Aadhar number of the vendor (optional).
        aadhar_image (JSONField): JSON data storing the Aadhar card image of 
                                  the vendor (optional).
        pancard_number (CharField): The PAN card number of the vendor (optional).
        pancard_image (JSONField): JSON data storing the PAN card image 
                                   of the vendor (optional).
        gst_number (CharField): The GST number of the vendor (optional).
        business_license (JSONField): JSON data storing the business license 
                                      information of the vendor (optional).
        is_verified (BooleanField): Indicates whether the vendor has been verified 
                                    by the system (default: False).
        is_document_added (BooleanField): Indicates whether the vendor has added 
                                          identification documents (default: False).
        bio (TextField): A brief biography or description of the vendor (optional).
        description (TextField): Additional description or information about the vendor (optional).

    Meta:
        db_table (str): The name of the database table for the model.
        verbose_name (str): The human-readable singular name for the model.
        verbose_name_plural (str): The human-readable plural name for the model.
    """

    user = models.OneToOneField(
        "authentication.User", on_delete=models.CASCADE, related_name="vendors"
    )
    shop_name = models.CharField(max_length=100, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    aadhar_image = models.JSONField(null=True, blank=True)
    pancard_number = models.CharField(max_length=10, blank=True)
    pancard_image = models.JSONField(null=True, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    business_license = models.JSONField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_document_added = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
