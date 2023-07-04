from django.shortcuts import render, redirect
from authentication.models import User
from django.views import View
from django.contrib import messages
from common.services import CloudinaryServices, HandelErrors
from .forms import VendorProfileForm, VendorProfileFormNameOnly, VendorAddressForm
from .models import Vendor, Address


def vendor_address(request):
    """
    View function for handling vendor address update.

    This function retrieves the vendor associated with the current user,
    validates the submitted address form, and updates the corresponding
    address record in the database. If any errors occur during form validation
    or database update, the errors are rendered along with the vendor data on
    the vendor.html template. Upon successful update, the function redirects
    to the vendor_profile view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the vendor_profile view.

    """
    vendor = Vendor.objects.get(user__id=request.user.id)

    form = VendorAddressForm(request.POST)
    if not form.is_valid():
        errors = HandelErrors.form_errors(form.errors, "dict")
        return render(
            request,
            "accounts/vendor.html",
            {"errors": errors, "data": vendor},
        )

    data = form.cleaned_data

    try:
        Address.objects.update_or_create(
            user=request.user,
            defaults={
                "address": data["address"],
                "pin_code": data["pin_code"],
                "city": data["city"],
                "state": data["state"],
                "country": data["country"],
            },
        )
        messages.success(request, "Address updated successfully")
    except:
        messages.error(request, "Something went wrong! Please try again.")

    return redirect("vendor_profile")


class VendorProfile(View):
    """
    A class-based view for managing the vendor profile.

    This view handles both GET and POST requests for the vendor profile page.
    It allows vendors to update their profile information, including shop name,
    personal name, and various documents such as Aadhar card, Pan card, and business license.

    Attributes:
        None

    Methods:
        get(request): Retrieves the vendor and address information and renders the vendor profile page.
        post(request): Handles the form submission for updating the vendor profile.

    """

    def get(self, request):
        """
        Retrieve the vendor and address information and render the vendor profile page.

        Args:
            request: The HTTP GET request object.

        Returns:
            A rendered HTML template displaying the vendor profile page with vendor and address data.

        """
        vendor = Vendor.objects.get(user__id=request.user.id)
        address = Address.objects.get(user=request.user)

        return render(
            request,
            "accounts/vendor.html",
            context={"data": vendor, "address": address},
        )

    def post(self, request):
        """
        Handle the form submission for updating the vendor profile.

        Args:
            request: The HTTP POST request object.

        Returns:
            If the form is valid and the profile update is successful, redirects to the vendor profile page.
            If the form is invalid, re-renders the vendor profile page with validation errors.

        """
        vendor = Vendor.objects.get(user__id=request.user.id)

        if vendor.is_document_added:
            # validate input data
            form = VendorProfileFormNameOnly(request.POST)

            if not form.is_valid():
                errors = HandelErrors.form_errors(form.errors, "dict")

                return render(
                    request,
                    "accounts/vendor.html",
                    {"errors": errors, "data": vendor},
                )

            data = form.cleaned_data

            # update data in database
            Vendor.objects.filter(user__id=request.user.id).update(
                shop_name=data["shop_name"]
            )
            User.objects.filter(id=request.user.id).update(name=data["name"])
            messages.success(request, "Profile updated successfully")
            return redirect("vendor_profile")

        # validate input data
        form = VendorProfileForm(request.POST, request.FILES)

        if not form.is_valid():
            errors = HandelErrors.form_errors(form.errors, "dict")

            return render(
                request,
                "accounts/vendor.html",
                {"errors": errors, "data": vendor},
            )

        data = form.cleaned_data

        # Store documents in cloudinary
        aadhar_image_url = CloudinaryServices.store_image(
            image=data["aadhar_image"], folder="vendors/" + vendor.shop_name + "/documents"
        )
        pancard_image_url = CloudinaryServices.store_image(
            image=data["pancard_image"], folder="vendors/" + vendor.shop_name + "/documents"
        )
        business_license_url = CloudinaryServices.store_image(
            image=data["business_license"], folder="vendors/" + vendor.shop_name + "/documents"
        )

        try:
            Vendor.objects.filter(user__id=request.user.id).update(
                shop_name=data["shop_name"],
                aadhar_number=data["aadhar_number"],
                pancard_number=data["pancard_number"],
                gst_number=data["gst_number"],
                aadhar_image=aadhar_image_url,
                pancard_image=pancard_image_url,
                business_license=business_license_url,
                is_document_added=True,
            )
            User.objects.filter(id=request.user.id).update(name=data["name"])

            messages.success(request, "Profile updated successfully")
        except:
            messages.error(request, "Something went wrong! Please try again.")

        return redirect("vendor_profile")
