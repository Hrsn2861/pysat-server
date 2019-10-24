"""tests for server config
"""
from django.test import TestCase

from server.models import ConfigHelper

class TestConfig(TestCase):
    """
    Test config for pysat server
    """

    def test_0001(self):
        """
        Test PhoneVerify Config
        """
        phone_verify = ConfigHelper.get_phone_verify_able()
        self.assertIn(phone_verify, [True, False])

    def test_0002(self):
        """
        Test New Config
        """
        newconfig = ConfigHelper.get_config('newconfig', 'newconfig')
        self.assertEqual(newconfig, 'newconfig')
        getconfig = ConfigHelper.get_config('newconfig', 'hello')
        self.assertEqual(getconfig, 'newconfig')
