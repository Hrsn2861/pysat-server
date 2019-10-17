"""tests for project
"""
from django.test import TestCase

import utils.response as Response
from utils.views import view_base
from utils.cipher import encrypt, decrypt
from utils.request import get_ip
from utils.tests.garbage import Garbage

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
        text = 'HelloWorld'
        encrypttext = encrypt(None)
        self.assertEqual(encrypttext, None)
        encrypttext = encrypt(text)
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
