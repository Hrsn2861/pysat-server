"""initialization for pytest

add some items into database for test
"""
from session.models import SessionHelper
from user.models import UserHelper
from user.models import EntryLogHelper
from utils import randkey

class Initialization:
    """initialization for pytest
    """
    IPADDR = 'for.test'
    TOKEN = randkey()

    @staticmethod
    def start_session():
        """start session for test
        """
        SessionHelper.add_session(Initialization.IPADDR, Initialization.TOKEN)
        session = SessionHelper.get_session_id(Initialization.TOKEN, Initialization.IPADDR)
        return session

    @staticmethod
    def register(username, password, phone, permission=8):
        """register
        """
        user = UserHelper.signup({
            'username' : username,
            'password' : password,
            'phone' : phone,
            'permission' : permission
        })
        return user

    @staticmethod
    def login(user_id, session):
        """login
        """
        EntryLogHelper.add_entrylog(session, user_id)

    @staticmethod
    def make_package(params):
        """get a package for functions
        """
        session = SessionHelper.get_session_id(Initialization.TOKEN, Initialization.IPADDR)
        user = UserHelper.get_user_by_session(session)
        return {
            'ip' : Initialization.IPADDR,
            'session' : session,
            'user' : user,
            'params' : params
        }
