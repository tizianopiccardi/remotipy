from tests import models
from remotipy.rpc import remote
from tests.models import UserModel


@remote("http://localhost:5000/method_dispatcher", models)
class DAO(object):

    def add_user(self, user):
        pass

#########################################
if __name__ == '__main__':
    user = UserModel({
                    'first_name': "John",
                    'last_name': "Brown",
                    'email': "my@email.me"
                    })
    # Call remote
    print DAO().add_user(user).message
