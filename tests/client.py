from tests import dto
from remotipy.rpc import remote, RemoteException
from tests.dto import UserModel


@remote("http://localhost:5000/method_dispatcher", dto)
class RemoteController(object):

    def my_remote_method(self, user):
        pass

    def my_remote_method_void(self, user):
        pass

    def my_missing_method(self):
        pass

    def my_method_with_errors(self):
        pass

#########################################
if __name__ == '__main__':
    user = UserModel({
                    'first_name': "John",
                    'last_name': "Brown",
                    'email': "my@email.me"
                    })
    # Call remote with result
    print RemoteController().my_remote_method(user).message

    # Call remote empty result
    RemoteController().my_remote_method_void(user)

    # Invoke a missing method
    try:
        RemoteController().my_missing_method()
    except RemoteException as e:
        print "Exception type: " + e.cls + " | Message: " + e.message

    # Invoke a method that may fail
    try:
        RemoteController().my_method_with_errors()
    except RemoteException as e:
        print "Exception type: " + e.cls + " | Message: " + e.message