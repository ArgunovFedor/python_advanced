import datetime
import unittest

from module_03_ci_culture_beginning.homework.person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        Person.__init__(self, name='TestUser', year_of_birth=datetime.datetime.strptime('1994-12-22', '%Y-%m-%d'),
                        address='someAddress')

    def test_get_age(self):
        expected_res = 27
        function_res = Person.get_age(self)
        assert expected_res == function_res, 'Not matched'

    def test_set_name(self):
        function_res = Person.set_name(self, 'Vasya')
        assert function_res is None

    def test_get_name(self):
        expected_res = 'TestUser'
        function_res = Person.get_name(self)
        assert expected_res == function_res, 'Not matched'

    def test_set_address(self):
        function_res = Person.set_address(self, address='testAddress')
        assert function_res is None

    def test_get_address(self):
        excepted_res = 'someAddress'
        function_res = Person.get_address(self)
        assert function_res == excepted_res, 'Not matched'

    def test_is_homeless(self):
        excepted_res = False
        function_res = Person.is_homeless(self)
        assert function_res == excepted_res, False