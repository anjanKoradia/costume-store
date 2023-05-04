from .validator import is_valid_email, CustomerSignupValidator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .models import User


class Auth(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("home_page")

        return render(req, "authentication/website/auth.html")

    def post(self, req):
        email = req.POST.get("email")

        if not is_valid_email(email):
            messages.error(req, "Please enter a valid email !!")
            return redirect("customer_auth")

        exists = User.objects.filter(email=email).exists()

        if exists:
            url = reverse("login")
        else:
            url = reverse("signup")

        return redirect(url + "?email=" + email)


class Login(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("home_page")

        return render(req, "authentication/website/login.html")

    def post(self, req):
        email = req.POST.get("email")
        password = req.POST.get("password")

        if not password:
            messages.error(req, "Password is required")
            url = reverse("login")
            return redirect(url + "?email=" + email)

        user = authenticate(req, email=email, password=password)
            
        if not user:
            messages.error(req, "Invalid Password")
            url = reverse("login")
            return redirect(url + "?email=" + email)

        login(req, user)
        
        if user.role == 'admin':
            return redirect(reverse('admin:index'))
        elif user.role == 'vendor':
            return redirect("home_page")
        
        return redirect("home_page")
        
        

class Signup(View):
    def get(self, req):
        if req.user.is_authenticated:
            return redirect("home_page")

        return render(req, "authentication/website/signup.html")

    def post(self, req):
        email = req.POST.get("email")
        name = req.POST.get("name")
        password = req.POST.get("password")
        cpassword = req.POST.get("cpassword")
        role = req.POST.get("role")

        # validate user input data
        validator = CustomerSignupValidator(
            {"name": name, "password": password, "confirm_pass": cpassword, "role": role}
        )
        status = validator.validate()

        if not status:
            error = validator.get_message_plain()
            for field in error:
                messages.error(req, error[field][0], field)

            url = reverse("signup")
            return redirect(url + "?email=" + email)

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                name = name,
                role = role
            )
            login(req, user)
            return redirect("home_page")
        except Exception as e:
            print(e.message)

def activate_user(req, email_token):
    try:
        user = User.objects.get(email_token=email_token)
        user.is_active = True
        user.save()
        login(req, user)
        return redirect('/')
    
    except Exception as e:
        return print(e)


def logout_user(req):
    logout(req)
    return redirect("home_page")
