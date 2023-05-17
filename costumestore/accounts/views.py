from .validator import validate_data, VendorDetailsSchema, VendorIdentitySchema
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from authentication.models import User
from django.contrib import messages
from django.views import View
from .models import Vendor


def is_vendor(user):
    return user.is_authenticated and user.role == "vendor"


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
class VendorProfile(View):
    def get(self, req):
        vendor = Vendor.objects.get(user_id=req.user.id)
        return render(req, "accounts/vendor.html", context={"vendor": vendor})

    def post(self, req):
        name: str = req.POST.get("name")
        shop_name: str = req.POST.get("shop_name")
        aadhar_number: int = req.POST.get("aadhar_number")
        pancard_number: int = req.POST.get("pancard_number")
        gst_number: int = req.POST.get("gst_number")
        aadhar_image: list = req.FILES.getlist("aadhar_image")
        pancard_image: list = req.FILES.getlist("pancard_image")
        business_license: list = req.FILES.getlist("business_license")

        vendor = Vendor.objects.get(user_id=req.user.id)
        if vendor.is_document_added:
            # validate input data
            errors = validate_data(
                VendorDetailsSchema,
                fields={
                    "name": name,
                    "shop_name": shop_name,
                },
            )
            if errors:
                messages.error(req, "errors")
                return redirect("vendor_profile")

            # update data in database
            Vendor.objects.filter(user_id=req.user.id).update(
                shop_name=shop_name,
            )
            User.objects.filter(id=req.user.id).update(name=name)

            return redirect("vendor_profile")

        # validate input data
        errors = validate_data(
            VendorIdentitySchema,
            fields={
                "name": name,
                "shop_name": shop_name,
                "aadhar_number": aadhar_number,
                "pancard_number": pancard_number,
                "gst_number": gst_number,
                "aadhar_image": aadhar_image,
                "pancard_image": pancard_image,
                "business_license": business_license,
            },
        )

        if errors:
            messages.error(req, "errors")
            return redirect("vendor_profile")

        try:
            Vendor.objects.filter(user_id=req.user.id).update(
                shop_name=shop_name,
                aadhar_number=aadhar_number,
                pancard_number=pancard_number,
                gst_number=gst_number,
                aadhar_image=aadhar_image,
                pancard_image=pancard_image,
                business_license=business_license,
                is_document_added = True
            )

            User.objects.filter(id=req.user.id).update(name=name)

        except Exception as e:
            print(e)

        return redirect("vendor_profile")
