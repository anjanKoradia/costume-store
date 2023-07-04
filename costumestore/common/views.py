from django.shortcuts import render

def error_404(request):
    return render(request, 'common/error_404.html', status=404)
