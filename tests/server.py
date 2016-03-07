from flask import Flask, request
from remotipy import rpc
from remotipy.rpc import response
from tests import dto
from tests.dto import Result


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
        raise TypeError("Something went wrong")

##########################################
app = Flask(__name__)


@app.route('/method_dispatcher', methods=['POST'])
def query():
    # check http header, cookies, etc
    result = rpc.dispatch(Controller, dto, request.get_data())
    return response(result)


if __name__ == '__main__':
    app.run(debug=True)
