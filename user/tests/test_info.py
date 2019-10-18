"""pytest for user.views.info
"""
from django.test import TestCase

from utils.tests.initialization import Initialization

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
