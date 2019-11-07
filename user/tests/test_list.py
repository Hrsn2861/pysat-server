"""pytest for user.views.list
"""
from django.test import TestCase

from utils.tests.initialization import Initialization
from utils.response import analyse_response

class TestUserListByRequest(TestCase):
    """
    Test user.list
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
        """Test request for list info
        """
        response = self.client.get('/user/list/get', {
            'token' : self.token,
            "show_invalid" : 'true',
            'manager_first' : 'true',
            'school_id' : 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(analyse_response(response).get('msg'), 'Success')
