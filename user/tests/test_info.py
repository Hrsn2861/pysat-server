"""pytest for user.views.info
"""
from django.test import TestCase

from utils.tests.initialization import Initialization
from utils.response import analyse_response

class TestUserInfoByRequest(TestCase):
    """
    Test user.info
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

    def test0001(self):
        """test user info get username is None
        """
        response = self.client.get('/user/info/get', {
            'token' : self.token
        })
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('msg'), 'Success')

    def test0002(self):
        """test user info for username is testuser
        """
        response = self.client.get('/user/info/get', {
            'token' : self.token,
            'username' : 'testuser'
        })
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('data').get('user').get('username'), 'testuser')
        self.assertEqual(data.get('data').get('user').get('phone'), '11011011011')

    def test0003(self):
        """test user info with no user
        """
        response = self.client.get('/user/info/get', {
            'token' : self.token,
            'username' : 'NoUser'
        })
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('msg'), 'No User')

    def test0004(self):
        """test user info modify_info
        """
        response = self.client.post('/user/info/modify', {
            'token' : self.token,
            'realname' : 'realtestname',
            'school' : 'tsinghua',
            'motto' : 'I am stupid'
        })
        self.assertEqual(response.status_code, 200)
        msg = analyse_response(response).get('msg')
        self.assertEqual(msg, 'Success')

    def test0005(self):
        """test user info modify_info with error
        """
        response = self.client.post('/user/info/modify', {
            'token' : self.token,
            'username'  : 'NoUser',
            'realname' : 'realtestname',
            'school' : 'tsinghua',
            'motto' : 'I am stupid'
        })
        self.assertEqual(response.status_code, 200)
        msg = analyse_response(response).get('msg')
        self.assertEqual(msg, 'No User')

    def test0006(self):
        """test user info set_phone
        """
        response = self.client.post('/user/info/setphone', {
            'token' : self.token,
            'phone' : '11012311011',
            'CAPTCHA' : 'GUXYNB'
        })
        self.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        self.assertEqual(data.get('msg'), 'CAPTCHA Error')
