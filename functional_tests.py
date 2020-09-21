"""
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
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        """Runs before each test"""
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Runs after each test"""
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Test method run by test runner"""
        # Z has just got home from work and needs to cook something fast before his
        # wife gets back from an all day shopping trip at PEP.
        # He desperately searches the internet and sees an interesting site called
        # "askfridge.com"
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention a fridge
        self.assertIn('Fridge', self.browser.title)
        # list of tags
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Fridge', header_text)

        # He is invited to enter an ingredient that is in his fridge
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an ingredient that is in your fridge'
        )

        # He types "Mince" into a text box (Z is still a student at heart)
        # send_keys is Selenium’s way of typing into input elements
        inputbox.send_keys('Mince')

        # When he hits enter, the page updates, and now the page lists
        # "1: Mince" as an item in an ingredient table
        # Keys class has special keys like Enter
        inputbox.send_keys(Keys.ENTER)
        # after Enter, the page will refresh.
        # time.sleep is there to make sure the browser has finished loading
        # before we make any assertions about the new page
        # This is a simple "explicit wait"
        # @TODO improve explicit wait for browser to load
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Mince' for row in rows)
        )

        # There is still a text box inviting him to add another ingredient.
        # He enters "Onions" (Z doesn't like food to go off)
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on his list


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main(warnings='ignore')
