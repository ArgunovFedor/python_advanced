import unittest

from module_04_flask.materials.get_requests import RegistrationForm, app


class TestCheckRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration/'

    def test_can_post_correct(self):
        sent = {'return_url': 'my_test_url'}
        response = self.app.post(self.base_url, data=sent)
        response_text = response.data.decode()
        # self.assertTrue(username in response_text)
        # self.assertTrue(day_to_word_map[current_day] in response_text)