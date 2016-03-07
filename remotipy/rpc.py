import json
import logging
import urllib3
import sys

http = urllib3.PoolManager(10)


def _remote_call(endpoint, models, extras, method, *params):
    """
    Private method: execute the remote method
    :param endpoint:
    :param models:
    :param extras:
    :param method:
    :param params:
    :return:
    """
    method_params = []

    for i in range(1, len(params)):
        method_params.append(params[i])
    req = {'method': method, 'params': method_params}
    logging.debug("REQUEST GET: " + endpoint)
    logging.debug("BODY: " + str(req))
    headers = {}
    if 'headers' in extras:
        headers = extras['headers']

    r = http.request('POST', endpoint,
                     headers=headers,
                     body=json.dumps(req, default=_object_serializer))
    content = r.data

    # print("RAW RESPONSE: " + str(content))
    return json.loads(content, object_hook=lambda x: _object_deserializer(models, x))


def _object_serializer(o):
    """
    Private method: Custom json serializer
    :param o:
    :return:
    """
    if isinstance(o, object) and hasattr(o, '__serializable__'):
        result = {'_class': o.__class__.__name__, '_data': o.__dict__}
        if isinstance(o, SerializableException):
            result['exception'] = True
        return result

# types that do not need complex in json (and not iterable)
primitive = (int, str, bool, float)


def is_primitive(thing):
    return isinstance(thing, primitive)


def _object_deserializer(models_module, obj):
    """
    Private method: Json deserializer
    :param models_module:
    :param obj:
    :return:
    """
    if obj is None or is_primitive(obj) or '_class' not in obj:
        return obj
    else:

        # if it's an exception the DTO is in this module (should be possible only on client side)
        if obj['_class'] == 'SerializableException' and obj['exception']:
            models_module = sys.modules[__name__]

        # get the class reference
        cls = getattr(models_module, obj['_class'])
        # instantiate the object
        result = cls()
        # fill the object
        for k, v in obj['_data'].iteritems():
            if isinstance(v, object):
                setattr(result, k, v)

        return result


def _query_decorator(func):
    """
    Private method: Call decorator
    :param func:
    :return:
    """
    def run_query(*v):
        response_object = _remote_call(
                                v[0].__rpc_endpoint__,
                                v[0].__models_module__,
                                v[0].__rpc_extras__,
                                func.__name__, *v)
        #return func(*v)
        if isinstance(response_object, SerializableException):
            raise RemoteException(response_object.message, response_object.cls)
        else:
            return response_object
    return run_query


def remote(endpoint, module, **extras):
    """
    Decorator used to declare a RPC class (class level)
    :param endpoint:
    :param module:
    :param extras:
    :return:
    """
    def decorate(cls):
        cls.__rpc_endpoint__ = endpoint
        cls.__rpc_extras__ = extras
        cls.__models_module__ = module
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, _query_decorator(getattr(cls, attr)))
        return cls
    return decorate


def serializable(original_class):
    """
    Decorator used to declare a serializable model (class level)
    :param original_class:
    :return:
    """
    orig_init = original_class.__init__

    # This pre-init is called both in standard initialization and from the json-to-object converter
    # (reason why we need support for empty constructor)
    def __init__(self, *args, **kws):
        setattr(original_class, "__serializable__", classmethod(lambda: True))

        try:
            # Call the original __init__
            orig_init(self, *args, **kws)
        except TypeError:
            raise TypeError("Number of arguments error. Does your class <" +
                            original_class.__name__ +
                            "> support empty __init__() call?")

    original_class.__init__ = __init__
    return original_class


def dispatch(controller_class, models_module, params):
    """
    Server side: dispatch the request to the destination method
    :param controller_class:
    :param models_module:
    :param params:
    :return:
    """
    req = json.loads(params)
    controller = controller_class()
    controller_method = req['method']
    params_list_dict = req['params']
    params_list = []
    for i in params_list_dict:
        obj = _object_deserializer(models_module, i)
        params_list.append(obj)

    try:

        if not hasattr(controller, controller_method):
            raise MethodNotFound(controller_method)

        method_reference = getattr(controller, controller_method)
        return method_reference(*params_list)

    except Exception as e:
        logging.error('Exception ' + e.__class__.__name__ +
                      ' managed in method ' + controller_method +
                      ": " + e.message)
        return SerializableException({'cls': e.__class__.__name__,
                                      'message': e.message})


def response(obj):
    """
    Format the response compatible with remotipy
    :param obj:
    :return:
    """
    return json.dumps(obj,  default=_object_serializer)


@serializable
class SerializableException(object):
    """
    Exception DTO
    """
    def __init__(self, info={}):
        self.cls = info.get('cls')
        self.message = info.get('message')


class MethodNotFound(Exception):
    """
    Raised when the requested method is not present in the remote controller (SERVER SIDE)
    """
    pass


class RemoteException(Exception):
    """
    Raised on the client side if we had an exception on the server
    """
    def __init__(self, message, cls):

        # Call the base class constructor with the parameters it needs
        super(RemoteException, self).__init__(message)
        self.cls = cls

    def __str__(self):
        return self.cls + ": " + self.message
