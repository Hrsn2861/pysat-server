"""tests for session
"""
from django.test import TestCase

from utils.response import analyse_response
from session.models import SessionHelper
from session.views import start_session

class TestSessionByRequest(TestCase):
    """
    Test session for pysat server session
    """

    def test_0001_startsession_error(self):
        """
        Test Start Session with Wrong-Request-Method
        """

    def test_0002_checksession_error(self):
        """
        Test Check Session Failed
        """
        token = 'hello world'
        response = self.client.get('/session/check', data={'token' : token})
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)

    def test_0003_checksession_error(self):
        """
        Test Check Session Failed
        """
        response = self.client.get('/session/check', data={})
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)

    def test_0004_checksession(self):
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

class TestSessionByCall(TestCase):
    """
    Test session for pysat server session
    """

    def test_0001(self):
        """
        Test GetSession Failed
        """
        ret = SessionHelper.get_session_id(None, None)
        self.assertEqual(ret, None)

    def test_0002(self):
        """
        Test GetSessionByID
        """
        ret = SessionHelper.get_session_by_id('1')
        self.assertEqual(ret, None)
        ret = SessionHelper.get_session_by_id(-1)
        self.assertEqual(ret, None)
        SessionHelper.add_session('IP')
        ret = SessionHelper.get_session_by_id(1)
        self.assertNotEqual(ret, None)

    def test_0003(self):
        """
        Test AddSession Failed
        """
        ret = SessionHelper.add_session(233)
        self.assertEqual(ret, None)

    def test_0004(self):
        """
        Test Disconnect Failed
        """
        ret = SessionHelper.disconnect(233, 666)
        self.assertEqual(ret, False)

    def test_0005(self):
        """
        Test Function `start_session`
        """
        response = start_session()
        self.assertEqual(response.status_code, 200)
