"""initialization for pytest

add some items into database for test
"""
from session.models import SessionHelper
from user.models import VerifyHelper, UserHelper
from utils.response import analyse_response
from utils.cipher import encrypt

class Initialization:
    """initialization for pytest
    """

    @staticmethod
    def start_session(testcase):
        """start session for test
        """
        response = testcase.client.post('/session/start')
        data = analyse_response(response)
        token = data.get('data').get('token')
        response = testcase.client.get('/myip')
        ip_addr = str(response.content, encoding="utf8")
        testcase.assertIsInstance(ip_addr, str)
        return token, ip_addr

    @staticmethod
    def disconnect(testcase):
        """disconnect session for test
        """
        ret = SessionHelper.disconnect(testcase.token, testcase.ip_addr)
        testcase.assertEqual(ret, True)

    @staticmethod
    def register(testcase, username, password, phone, permission=8):
        """register
        """
        response = testcase.client.post('/user/sign/verify', {
            'token' : testcase.token,
            'phone' : phone
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('status'), 1)

        session = SessionHelper.get_session_id(testcase.token, testcase.ip_addr)
        verifycode = VerifyHelper.get_latest_code(session, phone)
        testcase.assertNotEqual(verifycode, None)
        code = verifycode.get('code')

        response = testcase.client.post('/user/sign/register', {
            'token' : testcase.token,
            'username' : username,
            'password' : encrypt(password),
            'phone' : phone,
            'CAPTCHA' : code
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('status'), 1)

        user = UserHelper.get_user_by_username(username)
        UserHelper.modify_user(user['id'], {'permission' : permission})
        user = UserHelper.get_user_by_username(username)
        testcase.assertEqual(user['permission'], permission)

    @staticmethod
    def login(testcase, username, password):
        """register
        """
        response = testcase.client.post('/user/sign/login', {
            'token' : testcase.token,
            'username' : username,
            'password' : encrypt(password)
        })
        testcase.assertEqual(response.status_code, 200)
        data = analyse_response(response)
        testcase.assertEqual(data.get('status'), 1)
