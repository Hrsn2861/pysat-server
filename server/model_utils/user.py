from server.models import User


def getFirstUserInList(users):
    if len(users) > 0:
        ret = {
            'id': users[0].id,
            'username': users[0].username,
            'email': users[0].email,
            'telphone': users[0].telphone,
            'realname': users[0].realname,
            'school': users[0].school,
            'permission': users[0].permission,
        }
        return ret
    else:
        return None


def getUser(index):
    users = User.objects.filter(id=int(index))
    return getFirstUserInList(users)


def getUserByName(username):
    users = User.objects.filter(username=str(username))
    return getFirstUserInList(users)


def getUserByTelphone(telphone):
    users = User.objects.filter(telphone=str(telphone))
    return getFirstUserInList(users)


class UserInfoChecker:

    @staticmethod
    def check_password(password):
        return True

    @staticmethod
    def check_email(email):
        return True

    @staticmethod
    def check_realname(realname):
        return True

    @staticmethod
    def check_school(school):
        return True

    @staticmethod
    def check_telphone(telphone):
        return True