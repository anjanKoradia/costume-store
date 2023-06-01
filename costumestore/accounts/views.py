from .forms import VendorProfileForm, VendorProfileForm_Name_Only, VendorAddressForm
from costumestore.services import Cloudinary_Services
from django.shortcuts import render, redirect
from authentication.models import User
from django.views import View
from .models import Vendor, Address


def vendor_address(request):
    vendor = Vendor.objects.get(user__id=request.user.id)

    form = VendorAddressForm(request.POST)
    if not form.is_valid():
        errors = {}
        for field in form:
            if field.errors:
                errors[field.name] = field.errors[0]

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
    except Exception as e:
        print(e)

    return redirect("vendor_profile")


class Vendor_Profile(View):
    def get(self, request):
        vendor = Vendor.objects.get(user__id=request.user.id)
        address = Address.objects.get(user=request.user)

        return render(
            request,
            "accounts/vendor.html",
            context={"data": vendor, "address": address},
        )

    def post(self, request):
        vendor = Vendor.objects.get(user__id=request.user.id)

        if vendor.is_document_added:
            # validate input data
            form = VendorProfileForm_Name_Only(request.POST)

            if not form.is_valid():
                errors = {}
                for field in form:
                    if field.errors:
                        errors[field.name] = field.errors[0]

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

            return redirect("vendor_profile")

        # validate input data
        form = VendorProfileForm(request.POST, request.FILES)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]

            return render(
                request,
                "accounts/vendor.html",
                {"errors": errors, "data": vendor},
            )

        data = form.cleaned_data

        # Store documents in cloudinary
        aadhar_image_url = Cloudinary_Services.store_image(
            data["aadhar_image"], vendor.shop_name + "/documents"
        )
        pancard_image_url = Cloudinary_Services.store_image(
            data["pancard_image"], vendor.shop_name + "/documents"
        )
        business_license_url = Cloudinary_Services.store_image(
            data["business_license"], vendor.shop_name + "/documents"
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

        except Exception as e:
            print(e)

        return redirect("vendor_profile")
