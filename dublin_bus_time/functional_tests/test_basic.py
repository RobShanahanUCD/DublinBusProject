from selenium import webdriver
from django.test import TestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class FunctionalTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome( )

    def tearDown(self):
        self.browser.quit( )

    def test_twitter_feed(self):
        pass

    def test_template_ok(self):
        """Test the template rendering and simulate the user input"""

        self.browser.get('http://localhost:8000')
        self.assertIn('Dublin Bus', self.browser.title)

        new_items = ['Guinness Storehouse', 'Drumcondra']

        self.input_new_item(new_items[0], 'origin', 'Origin')
        self.input_new_item(new_items[1], 'destination', 'Destination')
        # self.check_prediction(new_items)

    def input_new_item(self, item, tag_id, placeholder):
        """Handle the dropdown list of the input box"""

        input_field = self.browser.find_element_by_id(tag_id)
        self.assertEqual(placeholder, input_field.get_attribute('placeholder'))
        input_field.send_keys(item)
        input_field.send_keys(Keys.DOWN)

        # class ="pac-container pac-logo hdpi"
        # wait for the first dropdown option to appear and open it
        first_option = WebDriverWait(input_field, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".pac-container li")))
        first_option.send_keys(Keys.RETURN)
        time.sleep(1)

    def check_prediction(self, new_items):
        pass
