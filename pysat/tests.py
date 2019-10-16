"""This is for pytest
"""

from django.test import TestCase
import pytest

@pytest.mark.django_db
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
