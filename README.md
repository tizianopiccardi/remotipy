# remotipy
Remote RPC over HTTP for python (v0.1)

### Step 1: Define the models (Client & Server)

In module *data.models* describe the models:

```python
@model
class UserModel(object):
    def __init__(self, params, login_provider=None):
        self.id = params.get('id')
        self.first_name = params.get('first_name')
        self.last_name = params.get('last_name')
        self.email = params.get('email')
```

Note: share this file both on the client and the server

### Step 2: Define empty stub client side (Client)

Use the decorator *@remote* to specify the rest endpoint and the module containing the models:

```python
from data import models

@remote("http://localhost:5000/method_dispatcher", models)
class DAO(object):

    def add_user(self, user):
        pass
```

Note: *@remote* supports custom HTTP headers using this format:
```python
@remote("http://localhost:5000/method_dispatcher", data.models, header={
            'X-Authentication-token': TokenGenerator.generate({'key': 123456789})
          })
```

### Step 3: Define the remote logic (Server)

Implement the actual logic

```python
class DAO(object):

    def add_user(self, user):
        # all your logic here
        result_object = UserDB.insert_one(user_document).id
        return result_object
```

### Step 4: Define the rest endpoint (Server)

Dispatch the body of the request to the invoked method. Here you can make the security checks (i.e. http headers).

```python
@app.route('/query', methods=['POST'])
def query():
    # dispatch format: controller_class, models_module, raw_body 
    result = rpc.dispatch(DAO, data.models, request.get_data())
    return json.dumps(result)
```

### Step 5: Enjoy

On the client now you can call:
```python
result = DAO().add_user(user)
```
