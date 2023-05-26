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
            if req.user.role == "admin":
                return redirect(reverse("admin:index"))
            elif req.user.role == "vendor":
                return redirect("dashboard")

            return redirect("home_page")
            
        response = render(req, "authentication/auth.html")
        return response

    def post(self, req):
        email = req.POST.get("email")

        if not is_valid_email(email):
            messages.error(req, "Please enter a valid email !!")
            return redirect("auth")

        exists = User.objects.filter(email=email).exists()

        if exists:
            response = render(
                req, "authentication/login.html", context={"email": email}
            )
        else:
            response = render(
                req, "authentication/signup.html", context={"email": email}
            )

        response["cache-control"] = "no-cache, no-store, must-revalidate"
        return response


def login_user(req):
    email = req.POST.get("email")
    password = req.POST.get("password")

    if not password:
        messages.error(req, "Password is required")
        return render(req, "authentication/login.html", context={"email": email})

    user = authenticate(req, email=email, password=password)

    if not user:
        messages.error(req, "Invalid Password")
        return render(req, "authentication/login.html", context={"email": email})

    login(req, user)

    if user.role == "admin":
        return redirect(reverse("admin:index"))
    elif user.role == "vendor":
        return redirect("dashboard")

    return redirect("home_page")


def register_user(req):
    email = req.POST.get("email")
    name = req.POST.get("name")
    password = req.POST.get("password")
    cpassword = req.POST.get("cpassword")
    role = req.POST.get("role")

    # validate user input data
    validator = CustomerSignupValidator(
        {
            "name": name,
            "password": password,
            "confirm_pass": cpassword,
            "role": role,
        }
    )
    status = validator.validate()

    if not status:
        validator_errors = validator.get_message_plain()
        errors = {}
        
        for e in validator_errors:
            errors[e] = validator_errors.get(e)[0]

        response = render(
            req,
            "authentication/signup.html",
            {"email": email, "name": name, "errors": errors},
        )
        response["cache-control"] = "no-cache, no-store, must-revalidate"
        return response

    try:
        User.objects.create_user(
            email=email, password=password, name=name, role=role
        )

        response = render(req, "authentication/success.html")
        response['cache-control'] = 'no-cache, no-store, must-revalidate'
        return response
    except Exception as e:
        print(e)


def activate_user(req, email_token):
    try:
        user = User.objects.get(email_token=email_token)
        if not user:
            messages.error(req, "Invalid Token")
            return redirect("auth")

        user.is_active = True
        user.save()
        login(req, user)
        messages.success(req, "Login successful")
        return redirect("/")

    except Exception as e:
        return print(e)


def logout_user(req):
    logout(req)
    return redirect("home_page")
