# from django.http import HttpResponse
from django.shortcuts import redirect, render
from fridge.models import Item


def home_page(request):
    """Home page view
     A view function has two jobs: processing user input,
    and returning an appropriate response.
    For home page that is storing the users' input to the database,
    and redirecting after a POST.
    TODO display mulitple lines in the table
    TODO different lists for different people
    """
    if request.method == 'POST':
        # .create creates a new Item, without needing to call .save()
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    """Render takes the request as its first parameter and the name of
    the template to render.
    Django will automatically search folders called templates inside any of
    your apps' directories.
    Then it builds an HttpResponse, based on the content of the template.
    """
    items = Item.objects.all()
    # render page with items from db
    return render(request, 'home.html', {'items': items})
