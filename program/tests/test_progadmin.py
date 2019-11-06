"""pytest for program.views.user
"""
from django.test import TestCase

from school.models import SchoolHelper, SubjectHelper
from program.models import ProgramHelper
from utils.tests.initialization import Initialization
from utils.response import analyse_response

class TestProgramUserByRequest(TestCase):
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
        Initialization.add_user_to_school(self, '测试大学')
        Initialization.submit_program(
            self, '测试代码', 'print("Hello World")', 'I am stupid', '测试大学', '计算机科学与技术'
            )

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test_0001(self):
        """this is a test for admin download
        """
        code_id = ProgramHelper.get_program_by_name('测试代码').get('id')
        response = self.client.get('/program/admin/download', {
            'token' : self.token,
            'code_id' : code_id
        })
        data = analyse_response(response)
        self.assertEqual(data.get('msg'), 'Success')

    def test0002(self):
        """this is a test for admin status
        """
        code_id = ProgramHelper.get_program_by_name('测试代码').get('id')
        source = 0
        target = 1
        response = self.client.post('/program/admin/status', {
            'token' : self.token,
            'code_id' : code_id,
            'source' : source,
            'target' : target
        })
        data = analyse_response(response)
        self.assertEqual(data.get('msg'), 'Status Changed Successful')
