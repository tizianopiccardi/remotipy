from flask import Flask, request
from remotipy import rpc
from remotipy.rpc import response
from tests import dto
from tests.dto import Result


class DAO(object):

    def my_remote_method(self, user):
        # all your logic here
        return Result(user.email+' DONE!')

##########################################
app = Flask(__name__)


@app.route('/method_dispatcher', methods=['POST'])
def query():
    # check http header, cookies, etc
    result = rpc.dispatch(DAO, dto, request.get_data())
    return response(result)


if __name__ == '__main__':
    app.run(debug=True)