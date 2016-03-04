# remotipy
Remote RPC over HTTP for python (v0.1.2) - Remote exception support

### Step 1: Define the DTO (Client & Server)

In module *data.dto* (example) describe the transfer objects (DTO):

```python
@serializable
class UserInfo(object):
    def __init__(self, params={}):
        self.first_name = params.get('first_name')
        self.last_name = params.get('last_name')
        self.email = params.get('email')
        
@serializable
class Result(object):
    def __init__(self, msg = None):
        self.message = msg
```

Note: share this file both on the client and the server

### Step 2: Define empty stub client side (Client)

Use the decorator *@remote* to specify the rest endpoint and the module containing the models:

```python
from data import models

@remote("http://localhost:5000/method_dispatcher", models)
class RemoteDAO(object):

    def my_remote_method(self, user):
        pass
```

Note: *@remote* supports custom HTTP headers using this format:
```python
@remote("http://localhost:5000/method_dispatcher", data.models, headers={
            'X-Authentication-token': TokenGenerator.generate({'key': 123456789})
          })
```

### Step 3: Define the remote logic (Server)

Implement the actual logic

```python
class DAO(object):

    def my_remote_method(self, user):
        # all your logic here
        return Result(user.email + ' DONE!')
```

### Step 4: Define the rest endpoint (Server)

You can use any python rest server to dispatch the body of the request to the invoked method. In this example we are using the Flask format.

```python
@app.route('/method_dispatcher', methods=['POST'])
def query():
    # check http header, cookies, etc
    # dispatch format: controller_class, models_module, raw_body 
    result = rpc.dispatch(DAO, models, request.get_data())
    return response(result)
```

Note: the function *response* is required to serialize back the response

### Step 5: Enjoy

On the client now you can call:
```python
result = DAO().my_remote_method(user)
```

--------

#### Known limitations:

The constructor ```def __init__(self, [ params={}, ... ] ) ``` of the serializable objects (step 1) **MUST** support the empty call.

#### FAQ: 
1. **How can I handle a remote exception?**
Remote exception are raised on the client side with type ```remotipy.rpc.RemoteException``` and you have access to the original message (```.message```) and the original class name (```.cls```)
2. **I get ```MethodNotFound: <my_remote_method>```. Why?**
Check the interface on the client side and the implementation on the server side have the same methods signatures: steps 2/3. 
(You could even copy same file on the client because the methods body is ignored)
3. **I'm using App Engine and I get ```TypeError('expected httplib.Message)```. Why?**
This is a known issue of urllib3&Python 2.7, to fix this go in ```<lib_dir_>/urllib3/util/response.py``` and remove from line 47 to 49.
