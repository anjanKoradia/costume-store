from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .validator import is_valid_email
from .forms import RegistrationForm
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .models import User


class Auth(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == "admin":
                return redirect(reverse("admin:index"))
            elif request.user.role == "vendor":
                return redirect("dashboard")

            return redirect("home_page")

        response = render(request, "authentication/auth.html")
        return response

    def post(self, request):
        email = request.POST.get("email")

        if not is_valid_email(email):
            messages.error(request, "Please enter a valid email !!")
            return redirect("auth")

        exists = User.objects.filter(email=email).exists()

        if exists:
            response = render(
                request, "authentication/login.html", {"data": {"email": email}}
            )
        else:
            response = render(
                request, "authentication/signup.html", {"data": {"email": email}}
            )

        response["cache-control"] = "no-cache, no-store, must-revalidate"
        return response


def login_user(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not password:
        messages.error(request, "Password is required")
        return render(request, "authentication/login.html", {"data": {"email": email}})

    user = authenticate(request, email=email, password=password)

    if not user:
        messages.error(request, "Invalid Password")
        return render(request, "authentication/login.html", {"data": {"email": email}})

    login(request, user)

    if user.role == "admin":
        return redirect(reverse("admin:index"))
    elif user.role == "vendor":
        return redirect("dashboard")

    return redirect("home_page")


def register_user(request):
    form = RegistrationForm(request.POST)

    if not form.is_valid():
        errors = {}
        for field in form:
            if field.errors:
                errors[field.name] = field.errors[0]
        return render(
            request,
            "authentication/signup.html",
            {
                "data": form.cleaned_data,
                "errors": errors,
            },
        )

    data = form.cleaned_data
    print(data, form.full_clean)

    try:
        User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            role=data["role"],
        )

        response = render(request, "authentication/success.html")
        response["cache-control"] = "no-cache, no-store, must-revalidate"
        return response
    except Exception as e:
        print(e)


def activate_user(request, email_token):
    try:
        user = User.objects.get(email_token=email_token)
        if not user:
            messages.error(request, "Invalid Token")
            return redirect("auth")

        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Login successful")
        return redirect("/")

    except Exception as e:
        return print(e)


def logout_user(request):
    logout(request)
    return redirect("home_page")
