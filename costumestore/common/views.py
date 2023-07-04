from django.shortcuts import render


def error_404(request):
    """
    View function to handle a 404 error.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 404 error page.

    """
    return render(request, "common/error_404.html", status=404)
