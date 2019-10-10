"""This is for pytest
"""

from django.test import TestCase

# Create your tests here.

class TestServer(TestCase):
    """
    TestCase for pysat server
    """

    def test_mainpage(self):
        """
        Test / GET
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
