from django.shortcuts import redirect


class PermissionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and self.check_user_permissions(request):
            response = self.get_response(request)
            return response

        if self.check_visitor_permissions(request):
            response = self.get_response(request)
            return response

        return redirect("home_page")
        

    def check_visitor_permissions(self, request):
        if request.path.find("visitor") == 1 or request.path == "/":
            return True

        return False

    def check_user_permissions(self, request):
        if (request.user.role == "vendor" or request.user.role == "admin") and (
            request.path.find("customer") == 1
        ):
            return False

        if (
            request.user.role == "customer" or request.user.role == "admin"
        ) and request.path.find("vendor") == 1:
            return False

        if (
            request.user.role == "customer" or request.user.role == "vendor"
        ) and request.path.find("admin") == 1:
            return False

        return True
