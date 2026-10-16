import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from changed import changed_services

SERVICES = ["a", "b"]


class ChangedTests(unittest.TestCase):
    def test_single_service(self):
        self.assertEqual(changed_services(["services/b/app.py"], SERVICES), ["b"])

    def test_two_services(self):
        self.assertEqual(changed_services(["services/a/x.py", "services/b/y.py"], SERVICES), ["a", "b"])

    def test_shared_means_everything(self):
        self.assertEqual(changed_services(["shared/util.py"], SERVICES), ["a", "b"])

    def test_docs_only_means_nothing(self):
        self.assertEqual(changed_services(["README.md", "docs/x.md"], SERVICES), [])

    def test_unknown_service_ignored(self):
        self.assertEqual(changed_services(["services/zzz/x.py"], SERVICES), [])


if __name__ == "__main__":
    unittest.main()
