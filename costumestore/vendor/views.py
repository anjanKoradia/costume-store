from .validator import ProductDetailsValidator,validate_data
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .models import Product, Vendor
from django.contrib import messages
from django.urls import reverse
from django.views import View
import cloudinary.uploader
from .forms import ProductDetails


def is_vendor(user):
    return user.is_authenticated and user.role == "vendor"


@user_passes_test(is_vendor, login_url="home_page")
def dashboard(req):
    vendor = Vendor.objects.get(user=req.user)
    products = Product.objects.filter(vendor=vendor).order_by("updated_at").reverse()[:10]

    return render(req, "vendor/dashboard.html", context={"products": products})


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
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
            return render(req, "vendor/add_product.html", {"errors": errors})
        
        data = form.cleaned_data
                
        try:
            vendor = Vendor.objects.get(user=req.user)

            images_url = []
            for image in images:
                result = cloudinary.uploader.upload(image, folder=vendor.shop_name+'/products',tags=[category,subcategory])
                result_dict = {"url": result["url"], "public_id": result["public_id"]}
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


@method_decorator(user_passes_test(is_vendor, login_url="home_page"), name="dispatch")
class Edit_Product(View):
    def get(self, req, id):
        product = Product.objects.get(pk=id)
        
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
            vendor = Vendor.objects.get(user=req.user)
            old_product = Product.objects.get(id=id)
            
            # store new images in cloudinary
            images_url = []
            for image in images:
                result = cloudinary.uploader.upload(image, folder=vendor.shop_name+'/products',tags=[category,subcategory])
                result_dict = {"url": result["url"], "public_id": result["public_id"]}
                images_url.append(result_dict)
            
            Product.objects.update_or_create(
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
                    "images":images_url,
                    "description":description,
               }
            )
            
            # delete old images from cloudinary
            for image in old_product.images:
                cloudinary.uploader.destroy(image["public_id"])

        except Exception as e:
            print(e)

        return redirect("dashboard")
