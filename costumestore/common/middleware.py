from django.shortcuts import redirect


class PermissionsMiddleware:
    """
    Middleware for handling user permissions in the application.

    This middleware checks the user's role and path to determine whether they have the necessary permissions to access
    certain parts of the application. If the user is authenticated and has the required permissions, the request is
    allowed to proceed. Otherwise, the user is redirected to the home page.

    Attributes:
        get_response (function): The next middleware or view function in the application's request-response chain.
    """

    def __init__(self, get_response):
        """
        Initialize the PermissionsMiddleware.

        Args:
            get_response (function): The next middleware or view function in the application's request-response chain.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request.

        If the user is authenticated and has the necessary permissions, the request is allowed to proceed. If the user
        is not authenticated or doesn't have the required permissions, they are redirected to the home page.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response generated by the view or middleware processing the request.
        """
        if request.user.is_authenticated and self.check_user_permissions(request):
            response = self.get_response(request)
            return response

        if self.check_visitor_permissions(request):
            response = self.get_response(request)
            return response

        return redirect("home_page")

    def check_visitor_permissions(self, request):
        """
        Check visitor permissions.

        Determine whether a visitor has permissions to access the current path. Visitors are allowed to access paths
        containing "visitor" or the root path ("/").

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            bool: True if the visitor has permissions, False otherwise.
        """
        if request.path.find("visitor") == 1 or request.path == "/":
            return True

        return False

    def check_user_permissions(self, request):
        """
        Check user permissions.

        Determine whether a user has permissions to access the current path based on their role. The roles "admin",
        "vendor", and "customer" have different access restrictions.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            bool: True if the user has permissions, False otherwise.
        """
        if request.user.role == "admin" and request.path.count("admin") != 0:
            return True

        if (request.user.role in ["vendor", "admin"]) and (
            request.path.count("customer") != 0
        ):
            return False

        if (request.user.role in ["customer", "admin"]) and request.path.count(
            "vendor"
        ) != 0:
            return False

        if (request.user.role in ["customer", "vendor"]) and request.path.count(
            "admin"
        ) != 0:
            return False

        return True