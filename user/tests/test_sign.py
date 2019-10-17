"""pytest for user.views.sign
"""
from django.test import TestCase

from utils.tests.initialization import Initialization

class TestUserSignByRequest(TestCase):
    """
    Test session for pysat server session
    """

    token = None
    ip_addr = None

    def setUp(self):
        """This will be called before test
        """
        self.token, self.ip_addr = Initialization.start_session(self)

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test_0001(self):
        """
        Test Register and Login
        """
        Initialization.register(self, 'testuser', 'Test666', '11011011011')
        Initialization.login(self, 'testuser', 'Test666')

