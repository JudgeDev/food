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
