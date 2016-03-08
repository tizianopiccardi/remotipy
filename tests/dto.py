from remotipy.rpc import serializable


@serializable
class UserModel(object):
    def __init__(self, params={}, login_provider=None):
        self.id = params.get('id')
        self.first_name = params.get('first_name')
        self.last_name = params.get('last_name')
        self.email = params.get('email')


@serializable
class ComplexObject(object):
    def __init__(self):
        self.string_field = "StringABC"
        self.int_field = 123
        self.list_field = ['much', 'wow', 'so', 'remotipy']
        self.object_field = UserModel({
                    'first_name': "Doge",
                    'last_name': "McDog",
                    'email': "doge@mcdog.me"
                    })


@serializable
class Result(object):
    def __init__(self, msg=None):
        self.message = msg
