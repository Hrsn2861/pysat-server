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
        """this is the test for create school
        """
        response = self.client.post('/school/school/create', {
            'token' : self.token,
            'username' : 'testuser',
            'school_name' : '新建大学',
            'school_description' : '新建一个大学'
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

    def test0002(self):
        """this is a school with duplicated name
        """
        response = self.client.post('/school/school/create', {
            'token' : self.token,
            'username' : 'testuser',
            'school_name' : '测试大学',
            'school_description' : '重复的名字'
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)

    def test0003(self):
        """this is a school with no headmaster
        """
        response = self.client.post('/school/school/create', {
            'token' : self.token,
            'username' : 'No User',
            'school_name' : '新建大学',
            'school_description' : '没有校长的大学'
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 0)
