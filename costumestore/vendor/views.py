from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product, Vendor
from .forms import ProductDetails
from django.views import View
import cloudinary.uploader


def dashboard(req):
    vendor = Vendor.objects.get(user=req.user)
    products = (
        Product.objects.filter(vendor=vendor).order_by("updated_at").reverse()[:10]
    )

    return render(req, "vendor/dashboard.html", context={"products": products})


class Store(ListView):
    model = Product
    template_name = "vendor/store.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)


def delete_product(req, id):
    Product.objects.get(id=id).delete()
    return redirect("dashboard")


class Add_Product(View):
    def get(self, req):
        return render(req, "vendor/add_product.html")

    def post(self, req):
        images = req.FILES.getlist("images")
        form = ProductDetails(req.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            return render(
                req,
                "vendor/add_product.html",
                {"data": form.cleaned_data, "errors": errors},
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=req.user)

            images_url = []
            if len(images) > 0:
                for image in images:
                    result = cloudinary.uploader.upload(
                        image,
                        folder=vendor.shop_name + "/products",
                        tags=[data["category"], data["subcategory"]],
                    )
                    result_dict = {
                        "url": result["url"],
                        "public_id": result["public_id"],
                    }
                    images_url.append(result_dict)

            Product.objects.create(
                vendor=vendor,
                name=data["name"],
                colors=data["colors"],
                dimension=data["dimension"],
                category=data["category"],
                subcategory=data["subcategory"],
                rating=data["rating"],
                price=data["price"],
                discount=data["discount"],
                stock=data["stock"],
                description=data["description"],
                images=images_url,
            )

        except Exception as e:
            print(e)

        return redirect("dashboard")


class Edit_Product(View):
    def get(self, req, id):
        product = Product.objects.get(pk=id)
        return render(
            req,
            "vendor/edit_product.html",
            context={"product": product},
        )

    def post(self, req, id):
        images = req.FILES.getlist("images")
        form = ProductDetails(req.POST)

        if not form.is_valid():
            errors = {}
            for field in form:
                if field.errors:
                    errors[field.name] = field.errors[0]
            form.cleaned_data["id"] = id
            return render(
                req,
                "vendor/edit_product.html",
                {"product": form.cleaned_data, "errors": errors},
            )

        data = form.cleaned_data

        try:
            vendor = Vendor.objects.get(user=req.user)
            old_product = Product.objects.get(id=id)

            # store new images in cloudinary
            images_url = []
            if len(images) > 0:
                for image in images:
                    result = cloudinary.uploader.upload(
                        image,
                        folder=vendor.shop_name + "/products",
                        tags=[data["category"], data["subcategory"]],
                    )
                    result_dict = {
                        "url": result["url"],
                        "public_id": result["public_id"],
                    }
                    images_url.append(result_dict)

            Product.objects.update_or_create(
                id=id,
                defaults={
                    "name": data["name"],
                    "colors": data["colors"],
                    "dimension": data["dimension"],
                    "category": data["category"],
                    "subcategory": data["subcategory"],
                    "rating": data["rating"],
                    "price": data["price"],
                    "discount": data["discount"],
                    "stock": data["stock"],
                    "description": data["description"],
                    "images": images_url,
                },
            )

            # delete old images from cloudinary
            for image in old_product.images:
                if image["public_id"]:
                    cloudinary.uploader.destroy(image["public_id"])

        except Exception as e:
            print(e)

        return redirect("dashboard")
