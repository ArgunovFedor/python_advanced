import datetime
import http
import unittest

from module_02_linux.homework.hw_3_2 import app


class Test_3_2(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = ''

    def test_check_add(self):
        ulr = '/add/2022-04-25/150'
        response = self.app.get(ulr)
        response_text = response.data.decode()
        self.assertTrue(http.HTTPStatus.OK, response_text)

    def test_check_calculate(self):
        url = '/calculate/1994'
        response = self.app.get(url)
        response_text = response.data.decode()
        self.assertTrue('150', response_text)
        self.assertTrue(http.HTTPStatus.OK, response_text)

    def test_check_add_date(self):
        ulr = '/add/21-12-1994/150'
        with self.assertRaises(ValueError):
            response = self.app.get(ulr)