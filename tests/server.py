import json

from flask import Flask, request
from remotipy import rpc
from remotipy.rpc import __object_serializer, response
from tests import models
from tests.models import Result


class DAO(object):

    def add_user(self, user):
        # all your logic here
        return Result({'status': 1, 'message': 'DONE!'})

##########################################
app = Flask(__name__)


@app.route('/method_dispatcher', methods=['POST'])
def query():
    # check http header, cookies, etc
    result = rpc.dispatch(DAO, models, request.get_data())
    return response(result)


if __name__ == '__main__':
    app.run(debug=True)