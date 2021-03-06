import logging

from tests import dto
from remotipy.rpc import remote, RemoteException
from tests.dto import UserModel, ComplexObject

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


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

    def my_method_with_complex_params(self, complex, extra_param1):
        pass

    def my_method_get_dict(self):
        pass

    @staticmethod
    def my_static_method(name):
        pass

    @staticmethod
    def my_static_empty_method():
        pass
#########################################
if __name__ == '__main__':
    user = UserModel({
                    'first_name': "John",
                    'last_name': "Brown",
                    'email': "my@email.me"
                    })

    # Test 1
    # Call remote with result
    print RemoteController().my_remote_method(user).message

    # Test 2
    # Call remote empty result
    RemoteController().my_remote_method_void(user)

    # Test 3
    # Invoke a missing method
    try:
        RemoteController().my_missing_method()
    except RemoteException as e:
        print "Exception type: " + e.cls + " | Message: " + e.message

    # Test 4
    # Invoke a method that may fail
    try:
        RemoteController().my_method_with_errors()
    except RemoteException as e:
        print "Exception type: " + e.cls + " | Message: " + e.message

    # Test 5
    # Call remote empty result
    complex_obj = ComplexObject()
    print RemoteController().my_method_with_complex_params(complex_obj, 1)

    # Test 6
    # Get a dictionary
    print RemoteController().my_method_get_dict()

    # Test 6
    # Static Method
    print RemoteController.my_static_method("Static!")

    # Test 7
    # Static Empty Method
    print RemoteController.my_static_empty_method()
