"""tests for project
"""
from django.test import TestCase

import utils.response as Response
from utils.views import view_base
from utils.cipher import AESCipher, decrypt
from utils.request import get_ip
from utils.uthelper.garbage import Garbage
from utils.uthelper.initialization import Initialization
from user.models import EntryLogHelper

class TestPySAT(TestCase):
    """
    Test for `pysat` folder
    """

    def test_0001(self):
        """
        Test /
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class TestUtils(TestCase):
    """
    Test for `utils`
    """

    def test_0001(self):
        """
        Test for `views.py`
        """
        response = view_base(None, None, 'METHOD', [], [])
        self.assertEqual(response.status_code, 200)

    def test_0002(self):
        """
        Test for `cipher.py`
        """
        cipher = AESCipher.cipher
        text = 'HelloWorld'
        encrypttext = cipher.encrypt(text)
        decrypttext = decrypt(encrypttext)
        self.assertEqual(decrypttext, text)
        failedtext = decrypt('helloworld')
        self.assertEqual(failedtext, None)
        failedtext = decrypt(None)
        self.assertEqual(failedtext, None)
        failedtext = decrypt('a9c423b717956255faceab65d2cc364a')
        self.assertEqual(failedtext, None)
        failedtext = decrypt(1)
        self.assertEqual(failedtext, None)

    def test_0003(self):
        """
        Test for `response.py`
        """
        response = Response.invalid_request()
        self.assertEqual(response.status_code, 200)
        response = Response.success_response(None)
        self.assertEqual(response.status_code, 200)
        response = Response.checked_response('')
        self.assertEqual(response.status_code, 200)
        response = Response.error_response('')
        self.assertEqual(response.status_code, 200)
        response = Response.failed_response('')
        self.assertEqual(response.status_code, 200)
        response = Response.make_response(None, None, None)
        self.assertEqual(response.status_code, 200)

    def test_0004(self):
        """
        Test for `request.py`
        """
        test = Garbage()
        test.META['REMOTE_ADDR'] = 'IP'
        self.assertEqual(get_ip(test), 'IP')
        test.META['HTTP_X_FORWARDED_FOR'] = 'IP2'
        self.assertEqual(get_ip(test), 'IP2')

class TestInitialization(TestCase):
    """
    Test for `utils.tests.initialization`
    """

    def test_0001(self):
        """
        Test
        """
        session = Initialization.start_session()
        self.assertNotEqual(session, None)
        user = Initialization.register('test', 'Test666', '110', 8)
        self.assertNotEqual(user, None)
        log1 = Initialization.login(user, session)
        log2 = EntryLogHelper.get_entrylog_by_user(user)
        Initialization.disconnect()
        self.assertEqual(log1, log2 is not None)
        package = Initialization.make_package(None)
        self.assertNotEqual(package, None)
