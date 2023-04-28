from django.shortcuts import render

def customer_auth_page(req):
    return render(req, "authentication/website/auth.html")