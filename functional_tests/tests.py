"""Functional tests
TODO different lists for different people
TODO refactor duplicates in urls

Run with: python manage.py test functional_tests

FTs could be in tests for the apps. Better to keep them separate,
because functional tests usually have cross-cutting concerns that
run across different apps. FTs are meant to see things from the point of view
of your users, and your users don’t care about how you’ve split work between
different apps.

The TDD approach wants our application to be covered by both types of test.
Our workflow will look a bit like this:

Start by writing a functional test, describing the new functionality from
the user’s point of view.

Once we have a functional test that fails, we start to think about how to
write code that can get it to pass (or at least to get past its current failure).
We now use one or more unit tests to define how we want our code to behave
— ​the idea is that each line of production code we write should be tested by
(at least) one of our unit tests.

Once we have a failing unit test, we write the smallest amount of
application code we can, just enough to get the unit test to pass.
We may iterate between steps 2 and 3 a few times, until we think the
functional test will get a little further.

Now we can rerun our functional tests and see if they pass,
or get a little further. That may prompt us to write some new unit tests,
and some new code, and so on.

All the way through, the functional tests are driving what development
we do from a high level, while the unit tests drive what we do at a low level.

Notes on functional testing:
Use a Functional Test to Scope Out a Minimum Viable App
== Acceptance Test == End-to-End Test
Don’t test constants, and testing HTML as text is a lot like testing a constant
"""

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
    """LiveServerTestCase will automatically create a test database
    (just like in a unit test run), and start up a development server for
    the functional tests to run against.
    """

    def setUp(self) -> None:
        """Runs before each test"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Runs after each test"""
        self.browser.quit()

    def test_layout_and_styling(self):
        # Z goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=100
        )
        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=100
        )

    def wait_for_row_in_list_table(self, row_text):
        """Wait for row to be loaded up to max timeout
         Replaces explicit wait
         """
        MAX_WAIT = 10  # max wait is 10 seconds

        start_time = time.time()
        while True:  # keep going unless row loaded or timeout
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            # catch wrong table or table not loaded and wait short time
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        """Test method run by test runner"""
        # Z has just got home from work and needs to cook something fast before his
        # wife gets back from an all day shopping trip at PEP.
        # He desperately searches the internet and sees an interesting site called
        # "askfridge.com"
        ## get url from LiveServerTestCase
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention a fridge
        self.assertIn('Fridge', self.browser.title)
        ## list of tags
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('fridge', header_text)

        # He is invited to enter an ingredient that is in his fridge
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an ingredient in your fridge'
        )

        # He types "Mince" into a text box (Z is still a student at heart)
        ## send_keys is Selenium’s way of typing into input elements
        inputbox.send_keys('Mince')

        # When he hits enter, the page updates, and now the page lists
        # "1: Mince" as an item in an ingredient table
        ## Keys class has special keys like Enter
        inputbox.send_keys(Keys.ENTER)
        ## after Enter, the page will refresh.
        ## time.sleep is there to make sure the browser has finished loading
        ## before we make any assertions about the new page
        ## This is a simple "explicit wait"
        self.wait_for_row_in_list_table('1: Mince')

        # There is still a text box inviting him to add another ingredient.
        # He enters "Onions" (Z doesn't like food to go off)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Onions')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on the list
        self.wait_for_row_in_list_table('1: Mince')
        self.wait_for_row_in_list_table('2: Onions')

        # Z wonders whether the site will remember the list.
        # Then he sees that the site has generated a unique URL
        # for him -- there is some explanatory text to that effect.
        # self.fail('Finish the test!')

        # He visits that URL - his to-do list is still there.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Z starts a new list of ingredients
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Mince')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Mince')

        # He notices that his list has a unique URL
        z_list_url = self.browser.current_url
        ## checks whether url string matches a regular expression
        self.assertRegex(z_list_url, '/fridge/.+')

        # Now a new user, W, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Z's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # W visits the home page.  There is no sign of Z's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Mince', page_text)
        self.assertNotIn('Onions', page_text)

        # W starts a new list by entering a new item. She is vegan and
        # less interesting than Z...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Goji berries')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Goji berries')

        # W gets her own unique URL
        w_list_url = self.browser.current_url
        self.assertRegex(w_list_url, '/fridge/.+')
        self.assertNotEqual(w_list_url, z_list_url)

        # Again, there is no trace of Z's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Mince', page_text)
        self.assertIn('Goji berries', page_text)

        # Satisfied, they both pour a drink and go to sit on the balcony.
