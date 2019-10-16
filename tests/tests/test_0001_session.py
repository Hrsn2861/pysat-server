"""tests for session
"""

from django.test import TestCase
import pytest

from utils.response import analyse_response

from session.models import SessionHelper

TOKEN = None

@pytest.mark.django_db
class TestSession(TestCase):
    """
    Test session for pysat server session
    """

    def test_0001_startsession(self):
        """
        Check start session
        """
        response = self.client.post('/session/start')
        self.assertEqual(response.status_code, 200)

    def test_0002_startsession_as_get(self):
        """
        Test Start Session with Wrong-Request-Method
        """
        response = self.client.get('/session/start')
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), -1)

    def test_0003_checksession(self):
        """
        Test Start and Check Session
        """
        token = SessionHelper.get_session_by_id(1).get('token')
        response = self.client.get('/session/check', data={'token' : token})
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)
