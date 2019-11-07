"""pytest for school.views.user
"""
from django.test import TestCase

from school.models import SchoolHelper, SubjectHelper
from program.models import ProgramHelper
from utils.tests.initialization import Initialization
from utils.response import analyse_response

class TestSchoolUser(TestCase):
    """
    Test Program User
    """

    token = None
    ip_addr = None

    def setUp(self):
        """This will be called before test
        """
        self.token, self.ip_addr = Initialization.start_session(self)
        Initialization.register(self, 'testuser', 'Test666', '11011011011')
        Initialization.login(self, 'testuser', 'Test666')
        Initialization.promote_user(self, 16)
        Initialization.create_school(self, '测试大学', '世界一流大学', 'testuser')
        Initialization.create_theme(self, '测试大学', '计算机科学与技术', '贵系', '2099-10-30 00:00:00.000000')

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test0001(self):
        """test for school user
        """
        school = SchoolHelper.get_school_by_name('测试大学')
        schoolid = school.get('id')
        response = self.client.post('/school/user/apply', {
            'token' : self.token,
            'apply_reason' : 'I am Stupid',
            'apply_school_id' : schoolid
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

    def test0002(self):
        """test for school user with some error
        """
        schoolid = -1
        response = self.client.post('/school/user/apply', {
            'token' : self.token,
            'apply_reason' : 'I am Stupid',
            'apply_school_id' : schoolid
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)
