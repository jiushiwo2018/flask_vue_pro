import pytest
import json

# class TestUserPassword(object):
#     @pytest.fixture
#     def users(self):
#         return json.loads(open('usersdev.json', 'r').read())
#
#     def test_user_password(self, users):
#         for user in users:
#             passwd = user['password']
#             assert len(passwd) >= 6
#             msg = "user %s has a weak password" %(user['name'])
#             assert passwd != 'password', msg
#             assert passwd != 'password123', msg

users = json.loads(open('usersdev.json', 'r').read())

class TestUserPasswordWithParam(object):

    # @pytest.fixture(params=users)
    # def user(self, request):
    #     return request.param

    @pytest.mark.parametrize("user", users)
    def test_user_password(self, user):
        passwd = user['password']
        assert len(passwd) >= 6
        msg = "user %s has a weak password" %(user['name'])
        assert passwd != 'password', msg
        assert passwd != 'password123', msg


# @pytest.fixture(scope="module",
#                 params=["smtp.gmail.com", "mail.python.org"])
# def smtp(request):
#     smtp = smtplib.SMTP(request.param, 587, timeout=5)
#     yield smtp
#     print ("finalizing %s" % smtp)
#     smtp.close()