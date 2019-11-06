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

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test_0001(self):
        """this is a test of school list
        """
        school = SchoolHelper.get_school_by_name('测试大学')
        school_id = school.get('id')
        theme = SubjectHelper.get_subject_by_name('计算机科学与技术')
        theme_id = theme.get('id')

        response = self.client.post('/program/user/submit', {
            'token' : self.token,
            'code_name'  : 'TestProgram',
            'code_content' : 'print("Hello World")',
            'code_readme' : 'Hello World',
            'school_id' : school_id,
            'theme_id' : theme_id
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

    def test_0002(self):
        """this is a test of like
        """
        school = SchoolHelper.get_school_by_name('测试大学')
        school_id = school.get('id')
        theme = SubjectHelper.get_subject_by_name('计算机科学与技术')
        theme_id = theme.get('id')

        response = self.client.post('/program/user/submit', {
            'token' : self.token,
            'code_name'  : 'TestProgram',
            'code_content' : 'print("Hello World")',
            'code_readme' : 'Hello World',
            'school_id' : school_id,
            'theme_id' : theme_id
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

        program = ProgramHelper.get_program_by_name('TestProgram')
        code_id = program.get('id')
        ProgramHelper.upload(code_id)

        response = self.client.post('/program/user/like', {
            'token' : self.token,
            'code_id' : code_id
        })

        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

    def test_0003(self):
        """this is a test of user download
        """
        school = SchoolHelper.get_school_by_name('测试大学')
        school_id = school.get('id')
        theme = SubjectHelper.get_subject_by_name('计算机科学与技术')
        theme_id = theme.get('id')

        response = self.client.post('/program/user/submit', {
            'token' : self.token,
            'code_name'  : 'TestProgram',
            'code_content' : 'print("Hello World")',
            'code_readme' : 'Hello World',
            'school_id' : school_id,
            'theme_id' : theme_id
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)

        program = ProgramHelper.get_program_by_name('TestProgram')
        code_id = program.get('id')

        response = self.client.get('/program/user/download', {
            'token' : self.token,
            'code_id' : code_id
        })

        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)
