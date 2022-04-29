import datetime
import unittest

from module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day import app, day_to_word_map


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def test_can_get_correct_username_with_weekdate(self):
        username = 'username'
        current_day = datetime.datetime.today().weekday()
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)
        self.assertTrue(day_to_word_map[current_day] in response_text)
