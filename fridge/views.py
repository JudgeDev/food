#from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_page(request):
    """Render takes the request as its first parameter
    and the name of the template to render.
    Django will automatically search folders called
    templates inside any of your apps' directories.
    Then it builds an HttpResponse, based on
    the content of the template."""
    return render(request, 'home.html')
