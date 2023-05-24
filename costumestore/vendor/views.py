from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Product, Vendor
from .validator import ProductDetailsValidator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View


def is_vendor(user):
    return user.is_authenticated and user.role == "vendor"


@user_passes_test(is_vendor, login_url="home_page")
def dashboard(req):
    vendor = Vendor.objects.get(user=req.user)
    products = Product.objects.filter(vendor=vendor).order_by("updated_at").reverse()

    return render(req, "vendor/dashboard.html", context={"products": products})


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
class Add_Product(View):
    def get(self, req):
        return render(req, "vendor/add_product.html")

    def post(self, req):
        name = req.POST.get("name")
        colors = req.POST.get("colors")
        dimension = req.POST.get("dimensions")
        category = req.POST.get("category")
        subcategory = req.POST.get("subcategory")
        rating = req.POST.get("rating")
        price = req.POST.get("price")
        discount = req.POST.get("discount")
        stock = req.POST.get("stock")
        description = req.POST.get("description")
        images = req.FILES.getlist("images")

        validator = ProductDetailsValidator(
            {
                "name": name,
                "category": category,
                "rating": rating,
                "price": price,
                "discount": discount,
                "stock": stock,
                "description": description,
                "images": images,
            }
        )

        status = validator.validate()
        if not status:
            error = validator.get_message_plain()
            for field in error:
                messages.error(req, error[field][0], field)

                return redirect("add_product")

        try:
            vendor = Vendor.objects.get(user=req.user)

            product = Product.objects.create(
                vendor=vendor,
                name=name,
                colors=colors,
                dimension=dimension,
                category=category,
                subcategory=subcategory,
                rating=rating,
                price=price,
                discount=discount,
                stock=stock,
                description=description,
            )

            # for img in images:
            #     ProductImage.objects.create(product=product, image=img)

        except Exception as e:
            print(e)

        return redirect("dashboard")


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
class Edit_Product(View):
    def get(self, req, id):
        product = Product.objects.get(pk=id)
        # images = ProductImage.objects.filter(product=product)

        return render(
            req,
            "vendor/edit_product.html",
            context={"product": product},
        )

    def post(self, req, id):
        name = req.POST.get("name")
        colors = req.POST.get("colors")
        dimension = req.POST.get("dimensions")
        category = req.POST.get("category")
        subcategory = req.POST.get("subcategory")
        rating = req.POST.get("rating")
        price = req.POST.get("price")
        discount = req.POST.get("discount")
        stock = req.POST.get("stock")
        description = req.POST.get("description")
        images = req.FILES.getlist("images")
        
        validator = ProductDetailsValidator(
            {
                "name": name,
                "category": category,
                "rating": rating,
                "price": price,
                "discount": discount,
                "stock": stock,
                "description": description,
            }
        )

        status = validator.validate()
        if not status:
            error = validator.get_message_plain()
            print(error)
            for field in error:
                messages.error(req, error[field][0], field)
                return redirect(reverse("edit_product", args={id}))

        try:
            product = Product.objects.update_or_create(
               id=id,
               defaults={
                    "name":name,
                    "colors":colors,
                    "dimension":dimension,
                    "category":category,
                    "subcategory":subcategory,
                    "rating":rating,
                    "price":price,
                    "discount":discount,
                    "stock":stock,
                    "description":description,
               }
            )
            
            # if images:
            #     ProductImage.objects.filter(product = product[0]).delete()

            #     for img in images:
            #         ProductImage.objects.create(product=product[0], image=img)
            

        except Exception as e:
            print(e)

        return redirect("dashboard")
