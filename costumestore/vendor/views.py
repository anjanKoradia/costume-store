from django.contrib.auth.decorators import login_required
from .validator import  CustomerSignupValidator
from django.shortcuts import render
from django.views import View

class Add_Product(View):
    def get(self, req):
        return render(req,'vendor/add_product.html')
    
    def post(self, req):
        name = req.POST.get('name')
        colors = req.POST.get('colors')
        dimension = req.POST.get('dimension')
        category = req.POST.get('category')
        subcategory = req.POST.get('subcategory')
        rating = req.POST.get('rating')
        price = req.POST.get('price')
        discount = req.POST.get('discount')
        description = req.POST.get('description')
        images = req.FILES.get('images')
        
        
        print(name, description, images, discount, colors, price, rating, dimension, category, subcategory, category)
        
        return render(req,'vendor/add_product.html')

@login_required(login_url='home_page')
def dashboard(req):
    return render(req, 'vendor/dashboard.html')

