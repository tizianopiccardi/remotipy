from tests import dto
from remotipy.rpc import remote
from tests.dto import UserModel


@remote("http://localhost:5000/method_dispatcher", dto)
class RemoteDAO(object):

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
    print RemoteDAO().add_user(user).message
