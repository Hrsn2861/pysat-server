"""pytest for program.views.user
"""
from django.test import TestCase

from utils.tests.initialization import Initialization
from utils.response import analyse_response
from program.models import ProgramHelper

class TestProgUserByRequest(TestCase):
    """
    Test program.user
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
        """Test submit like and download
        """
        response = self.client.post('/program/user/submit', {
            'token' : self.token,
            'codename' : 'Test codename',
            'code' : 'Test code',
            'readme' : 'Test readme',
            'theme' : 1,
            'schoolid' : 1
        })
        self.assertEqual(response.status_code, 200)
        response = analyse_response(response)
        self.assertEqual(response.get('status'), 1)

    def test_0002(self):
        """Test like user without permission
        """
        prog_id = ProgramHelper.add_program('1', 'Testname', 'GUXYNB', 'readme', 1, 1)
        response = self.client.post('/program/user/like', {
            'token' : self.token,
            'codeid' : prog_id
        })
        self.assertEqual(response.status_code, 200)
        response = analyse_response(response)
        self.assertEqual(response.get('status'), 0)

    def test_0003(self):
        """Test download
        """
        prog_id = ProgramHelper.add_program('1', 'Testname', 'GUXYNB', 'readme',1 ,1)
        response = self.client.get('/program/user/download', {
            'token' : self.token,
            'codeid' : prog_id
        })
        self.assertEqual(response.status_code, 200)
        response = analyse_response(response)
        self.assertEqual(response.get('status'), 1)


    def test_0004(self):
        """test for like and download with no program
        """
        response = self.client.post('/program/user/like', {
            'token' : self.token,
            'codeid' : '112233'
        })
        self.assertEqual(response.status_code, 200)
        response = analyse_response(response)
        self.assertEqual(response.get('status'), 0)

    def test_0005(self):
        """test for like download with no program
        """
        response = self.client.get('/program/user/download', {
            'token' : self.token,
            'codeid' : '112233'
        })
        self.assertEqual(response.status_code, 200)
        response = analyse_response(response)
        self.assertEqual(response.get('status'), 0)
