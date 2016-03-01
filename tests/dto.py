from remotipy.rpc import serializable


@serializable
class UserModel(object):
    def __init__(self, params, login_provider=None):
        self.id = params.get('id')
        self.first_name = params.get('first_name')
        self.last_name = params.get('last_name')
        self.email = params.get('email')


@serializable
class Result(object):
    def __init__(self, params):
        self.status = params.get('status')
        self.message = params.get('message')
