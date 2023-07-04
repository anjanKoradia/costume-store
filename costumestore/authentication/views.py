from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from costumestore.services import HandelErrors
from .validator import is_valid_email
from .forms import RegistrationForm
from .models import User


class Auth(View):
    """
    Authentication view for handling user login and signup.

    This view handles GET and POST requests for user authentication.

    GET: If the user is already authenticated, it redirects them to the appropriate
    page based on their role. Otherwise, it renders the authentication page.

    POST: Validates the email provided in the request, and redirects to the
    appropriate page based on its existence. If the email exists in the database,
    it renders the login page with the email pre-filled.
    """

    def get(self, request):
        """
        Handles GET requests for user authentication.

        If the user is already authenticated, it redirects them to the appropriate page based on their role.
        Otherwise, it renders the authentication page.

        Args:
            request: The request object.

        Returns:
            A redirect response or a rendered response.
        """
        if request.user.is_authenticated:
            if request.user.role == "admin":
                return redirect(reverse("admin:index"))

            if request.user.role == "vendor":
                return redirect("dashboard")

            return redirect("home_page")

        response = render(request, "authentication/auth.html")
        return response

    def post(self, request):
        """
        Handles POST requests for authentication.

        Retrieves the email from the request's POST data.
        Checks if the email is valid.
        - If the email is invalid, displays an error message and redirects to the auth page.
        - Checks if a user with the given email already exists.
          - If a user exists, renders the login.html template with the email data.
          - If a user doesn't exist, renders the signup.html template with the email data.

        Returns:
        - If a user with the given email exists, renders the login.html template.
        - If a user with the given email doesn't exist, renders the signup.html template.
        """
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
    """
    Authenticates and logs in a user based on the provided email and password.

    Args:
        request (HttpRequest): The HTTP request object containing user data.

    Returns:
        HttpResponse: The response object based on the login outcome.
    """
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

    if user.role == "vendor":
        return redirect("dashboard")

    return redirect("home_page")


def register_user(request):
    """
    Register a user based on the provided registration form data.

    Args:
        request: The HTTP request object containing the form data.

    Returns:
        A rendered HTTP response indicating success or displaying form errors.

    """
    form = RegistrationForm(request.POST)

    if not form.is_valid():
        errors = HandelErrors.form_errors(form.errors, "dict")
        return render(
            request,
            "authentication/signup.html",
            {
                "data": form.cleaned_data,
                "errors": errors,
            },
        )

    data = form.cleaned_data

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
    """
    Activate a user account using the provided email token.

    Args:
        request (HttpRequest): The HTTP request object.
        email_token (str): The email token used to activate the user account.

    Returns:
        HttpResponseRedirect: A redirect response to the appropriate page.

    Raises:
        Exception: If any error occurs during the activation process.
    """
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
    """
    Log out the currently authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect response to the home page.

    """
    logout(request)
    return redirect("home_page")
