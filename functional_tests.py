from selenium import webdriver
import unittest


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
        self.fail('Finish the test...')

        # He is invited to enter ...


if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main(warnings='ignore')
