"""Unit tests for fridge app
Run with: python manage.py test fridge

The Unit-Test/Code Cycle:

In the terminal, run the unit tests and see how they fail.

In the editor, make a minimal code change to address the current test failure.

Repeat!

Triangulation
The unit-test/code cycle: Red, Green, Refactor:

Start by writing a unit test which fails (Red).

Write the simplest possible code to get it to pass (Green),
even if that means cheating.

Refactor to get to better code that makes more sense.

What justifies moving from an implementation where we "cheat" to one we’re happy with?

One methodology is eliminate duplication:

if your test uses a magic constant (like the "1:" in front of our list item),
and your application code also uses it, that counts as duplication,
so it justifies refactoring.
Removing the magic constant from the application code usually means
you have to stop cheating.

If that leaves things a little too vague, use a second technique,
which is called triangulation:
If your tests let you get away with writing "cheating" code that you’re
not happy with, like returning a magic constant, write another test that
forces you to write some better code.
That’s what we’re doing when we extend the FT to check that we get a "2:"
when inputting a second list item.

Refactoring:
Improve the code without changing its functionality When refactoring,
work on either the code or the tests, but not both at once.
Test before refactoring.
Commit after refactoring.

Three Strikes and Refactor
- applies Don’t Repeat Yourself (DRY):

Code smell in FT:
Three almost identical code blocks doing the same thing.
You can copy and paste code once, and it may be premature to try
to remove the duplication it causes, but once you get three occurrences,
it’s time to remove duplication.

A long unit test either needs to be broken into two, or it may be
an indication that the thing you’re testing is too complicated.

Integrated tests
Technically a test that relies on an external system, e.g. a database,
is called an integrated test.
"""

from django.test import TestCase
# from django.http import HttpRequest

from fridge.models import Item, List


class HomePageTest(TestCase):

    """ Old test
    def test_root_url_resolves_to_home_page_view(self):
        # find what view function url should map to
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    """

    def test_uses_home_template(self):
        # Instead of manually creating an HttpRequest object and calling
        # the view function directly, call self.client.get,
        # passing it the URL to test.
        response = self.client.get('/')
        """ Old method using HttpRequest
        # HttpRequest object is what Django sees when a user’s browser asks
        # for a page
        request = HttpRequest()
        # pass it to a view, which gives a response - instance of HttpResponse
        response = home_page(request)
        """
        # convert raw bytes to html
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Ask Fridge</title>', html)
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        """To do a POST, call self.client.post.
        It takes a data argument which contains the form data we want to send.
        Then check that the text from our POST request ends up in
        the rendered HTML.
        """
        response = self.client.post('/fridge/new',
                                    data={'item_text': 'A new list item'})
        # = objects.all().count()
        self.assertEqual(Item.objects.count(), 1)
        # = objects.all()[]
        new_item = Item.objects.first()
        # check item's text is correct
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/fridge/new',
                                    data={'item_text': 'A new list item'})
        # check for redirect after POST
        # assertRedirects replaces assertEqual of 302 code
        new_list = List.objects.first()
        # redirect to url of new list
        self.assertRedirects(response,
                             f'/fridge/{new_list.id}/')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/fridge/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/fridge/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/fridge/{correct_list.id}/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        # create a new list
        list_ = List.objects.create()
        # point test to url with id of list
        response = self.client.get(f'/fridge/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        # setup test
        # create parent list
        correct_list = List.objects.create()
        # create items on list
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        # create another list
        other_list = List.objects.create()
        # ...with two different items
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        # exercise code under test
        response = self.client.get(f'/fridge/{correct_list.id}/')

        # assert results
        # assertContains(r, 'text') replaces
        # self.assertIn('text', r.content.decode())
        # checks items on the correct list are there
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        # ...and not those on the other list
        self.assertNotContains(response, 'other itemey 1')
        self.assertNotContains(response, 'other itemey 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/fridge/{correct_list.id}/')
        # context passed to the render function is put
        # on the response object to help with testing
        self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelsTest(TestCase):
    """Testing with Object-Relational Mapper (ORM)
    ORM is a layer of abstraction for data stored in
    a database with tables, rows, and columns.
    It lets us work with databases using familiar
    object-oriented metaphors which work well with code.
    Classes map to database tables, attributes map to columns,
    and an individual instance of the class represents
    a row of data in the database.
    """

    def test_saving_and_retrieving_items(self):
        # create a new list in the database
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        # assign list to item .list property
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        # assign list to item .list property
        second_item.list = list_
        second_item.save()

        # check list is properly saved
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        # query the database via the class attribute, .objects
        saved_items = Item.objects.all()
        # returns list-like object called a QuerySet
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,
                         'The first (ever) list item')
        # check item is assigned to list
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text,
                         'Item the second')
        # check item is assigned to list
        self.assertEqual(second_saved_item.list, list_)
