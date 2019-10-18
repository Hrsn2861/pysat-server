"""pytest for user.views.sign
"""
from django.test import TestCase

from utils.cipher import encrypt
from utils.response import analyse_response
from utils.tests.initialization import Initialization

class TestUserSignByRequest(TestCase):
    """
    Test user.sign
    """

    token = None
    ip_addr = None

    def setUp(self):
        """This will be called before test
        """
        self.token, self.ip_addr = Initialization.start_session(self)
        Initialization.register(self, 'testuser', 'Test666', '11011011011')
        Initialization.login(self, 'testuser', 'Test666')

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test_0001(self):
        """
        Test Logout
        """
        Initialization.logout(self)

    def test_0002(self):
        """
        Test some failed situations for register
        """
        response = self.client.post('/user/sign/register', {
            'token' : self.token,
            'username' : 'testuser',
            'password' : encrypt('Password233'),
            'phone' : '11223344556',
            'CAPTCHA' : 'Hello'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'Username exists')
        response = self.client.post('/user/sign/register', {
            'token' : self.token,
            'username' : 'testuser2',
            'password' : encrypt('Password233'),
            'phone' : '11223344556',
            'CAPTCHA' : 'Hello'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'CAPTCHA Error')

    def test_0003(self):
        """
        Test some failed situations for login
        """
        response = self.client.post('/user/sign/login', {
            'token' : self.token,
            'username' : 'testuser2',
            'password' : encrypt('Password233'),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'NoUser')
        response = self.client.post('/user/sign/login', {
            'token' : self.token,
            'username' : 'testuser',
            'password' : encrypt('Password233')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'PasswordError')

    def test_0004(self):
        """
        Test some failed situations for verifyphone
        """
        response = self.client.post('/user/sign/verify', {
            'token' : self.token,
            'phone' : '11011011011'
        })
        response = self.client.post('/user/sign/verify', {
            'token' : self.token,
            'phone' : '11011011011'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'RequestTooFrequently')
