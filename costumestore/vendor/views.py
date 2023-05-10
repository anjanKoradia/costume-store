from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .validator import ProductDetailsValidator
from django.shortcuts import render, redirect
from .models import Product, ProductImage
from django.contrib import messages
from django.views import View


def is_vendor(user):
    return user.is_authenticated and user.role == "vendor"


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
class Add_Product(View):
    def get(self, req):
        return render(req, "vendor/add_product.html")

    def post(self, req):
        name = req.POST.get("name")
        colors = req.POST.get("colors")
        dimension = req.POST.get("dimension")
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
            product = Product.objects.create(
                name=name,
                colors=colors,
                dimension=dimension,
                category=category,
                subcategory=subcategory,
                price=price,
                discount=discount,
                stock=stock,
                description=description,
            )

            for img in images:
                image = ProductImage.objects.create(image=img)
                product.images.add(image)

        except Exception as e:
            print(e)

        return redirect("dashboard")


@user_passes_test(is_vendor, login_url="home_page")
def dashboard(req):
    return render(req, "vendor/dashboard.html")
