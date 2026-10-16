import unittest

from app import name


class B(unittest.TestCase):
    def test_name(self):
        self.assertEqual(name(), "service-b")
