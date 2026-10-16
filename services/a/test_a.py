import unittest

from app import name


class A(unittest.TestCase):
    def test_name(self):
        self.assertEqual(name(), "service-a")
