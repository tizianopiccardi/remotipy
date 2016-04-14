import logging

from flask import Flask, request
from remotipy import rpc
from remotipy.rpc import response
from tests import dto
from tests.dto import Result

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Controller(object):

    def my_remote_method(self, user):
        # all your logic here
        print 'Executing my_remote_method'
        return Result(user.email+' DONE!')

    def my_remote_method_void(self, user):
        # all your logic here
        print 'Executing my_remote_method_void: ' + user.first_name
        return

    def my_method_with_errors(self):
        raise TypeError("Something went wrong as expected")

    def my_method_with_complex_params(self, complex, extra_param1):
        if extra_param1 == 1:
            return complex.object_field.first_name
        else:
            return 'Some error message'

    def my_method_get_dict(self):
        return {'value1': 1, 'value2': 2}

##########################################
app = Flask(__name__)


@app.route('/method_dispatcher', methods=['POST'])
def query():
    # check http header, cookies, etc
    result = rpc.dispatch(Controller, dto, request.get_data())
    return response(result)


if __name__ == '__main__':
    app.run(debug=True)
