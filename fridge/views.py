# from django.http import HttpResponse
from django.shortcuts import redirect, render
from fridge.models import Item, List


def home_page(request):
    """Home page view
     A view function has two jobs: processing user input,
    and returning an appropriate response.
    For home page that is storing the users' input to the database,
    and redirecting after a POST.

    Render takes the request as its first parameter and the name of
    the template to render.
    Django will automatically search folders called templates inside any of
    your apps' directories.
    Then it builds an HttpResponse, based on the content of the template.
    """
    return render(request, 'home.html')


def new_list(request):
    """New list view page"""
    # create new list
    list_ = List.objects.create()
    # create new item from post request and associate it with the list
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/fridge/{list_.id}/')


def view_list(request, list_id):
    """View for a list"""
    list_ = List.objects.get(id=list_id)
    # render page with items from db
    return render(request, 'list.html', {'list': list_})

def add_item(request, list_id):
    """Add an item to a fridge list"""
    list_ = List.objects.get(id=list_id)
    # save new list item
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/fridge/{list_.id}/')



