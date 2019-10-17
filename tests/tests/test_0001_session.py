"""tests for session
"""

from django.test import TestCase

from utils.response import analyse_response

TOKEN = None

class TestSession(TestCase):
    """
    Test session for pysat server session
    """

    def test_0001_startsession_error(self):
        """
        Test Start Session with Wrong-Request-Method
        """
        response = self.client.get('/session/start')
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), -1)

    def test_0002_checksession_error(self):
        """
        Test Check Session
        """
        token = 'hello world'
        response = self.client.get('/session/check', data={'token' : token})
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)

    def test_0003_checksession(self):
        """
        Test Start and Check Session
        """
        response = self.client.post('/session/start')
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)
        token = data.get('data').get('token')
        response = self.client.get('/session/check', data={'token' : token})
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)
