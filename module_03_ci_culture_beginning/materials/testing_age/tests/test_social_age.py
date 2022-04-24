import unittest

from social_age import get_social_status


class TestSocialAge(unittest.TestCase):
    def test_can_get_child_age(self):
        age = 8
        expected_res = 'ребенок'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_can_get_teenager(self):
        age = 13
        expected_res = 'подросток'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_man(self):
        age = 27
        expected_res = 'взрослый'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_old_man(self):
        age = 55
        expected_res = 'пожилой'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_too_old_man(self):
        age = 100
        expected_res = 'пенсионер'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_cannot_pass_str_as_age(self):
        age = 'old'
        with self.assertRaises(ValueError):
            get_social_status(age)
