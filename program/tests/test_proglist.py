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
        Initialization.create_theme(self, 0, '在野主题', '在野主题', '2099-10-30 00:00:00.000000')
        Initialization.add_user_to_school(self, '测试大学')
        Initialization.submit_program(
            self, '测试代码', 'print("Hello World")', 'I am stupid', '测试大学', '计算机科学与技术'
            )
        Initialization.submit_program(
            self, '在野代码', 'print("Test code")', 'I am not stupid', 0, '在野主题'
        )

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)
