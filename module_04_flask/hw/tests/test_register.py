import unittest

from module_04_flask.hw.hw_1_2 import RegistrationForm, app


class TestCheckRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_positive(self):
        sent = {
            'email':'test@mail.ru',
            'phone':'7912123451',
            'name': 'TestName',
            'address': 'TestAddress',
            'index': '777',
            'comment': 'TestComment'
        }
        response = self.app.post(self.base_url, data=sent)
        self.assertTrue(response.status_code, '200')

    def test_negative_bad_arg_email(self):
        sent = {
            'email': 'testmail.ru',
            'phone': '7912123451',
            'name': 'TestName',
            'address': 'TestAddress',
            'index': '777',
            'comment': 'TestComment'
        }
        response = self.app.post(self.base_url, data=sent)
        self.assertTrue(response.status_code, '400')

    def test_negative_bad_arg_phone(self):
        sent = {
            'email':'test@mail.ru',
            'phone':'1234',
            'name': 'TestName',
            'address': 'TestAddress',
            'index': '777',
            'comment': 'TestComment'
        }
        response = self.app.post(self.base_url, data=sent)
        self.assertTrue(response.status_code, '400')

    def test_negative_bad_args(self):
        sent = {
            'email': '',
            'phone': '',
            'name': '',
            'address': '',
            'index': '',
            'comment': ''
        }
        response = self.app.post(self.base_url, data=sent)
        self.assertTrue(response.status_code, '400')