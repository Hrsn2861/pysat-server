"""pytest for school.views.theme
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
        Initialization.promote_user(self, 2)
        # Initialization.create_school(self, '测试大学', '世界一流大学', 'testuser')
        Initialization.create_theme(self, 0, '计算机科学与技术', '贵系', '2099-10-30 00:00:00.000000')

    def tearDown(self):
        """This will be called after test
        """
        Initialization.disconnect(self)

    def test0001(self):
        """test error of create theme
        """
        response = self.client.post('/school/theme/create', {
            'token' : self.token,
            'school_id' : 0,
            'theme_name' : '测试帖子',
            'theme_description' : '测试帖子',
            'theme_deadline' : '2019-10-30 00:00:00.000000'
        })
        data = analyse_response(response)
        self.assertEqual(data.get('status'), 1)
