import json
import logging
import urllib2


def __remote_call(endpoint, models, extras, method, *params):
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
    request = urllib2.Request(endpoint,
                              headers=headers,
                              data=json.dumps(req, default=__object_serializer))
    content = urllib2.urlopen(request).read()
    logging.debug("RAW RESPONSE: " + str(content))
    return json.loads(content, object_hook=lambda x: __object_deserializer(models, x))


def __object_serializer(o):
    """
    Private method: Custom json serializer
    :param o:
    :return:
    """
    if isinstance(o, object) and hasattr(o, '__serializable__'):
        return {'_class': o.__class__.__name__, '_data': o.__dict__}


def __object_deserializer(models_module, obj):
    """
    Private method: Json deserializer
    :param models_module:
    :param obj:
    :return:
    """
    if obj is None or '_class' not in obj:
        return obj
    else:
        cls = getattr(models_module, obj['_class'])
        result = cls(obj['_data'])
        for k, v in obj['_data'].iteritems():
            if isinstance(v, object):
                setattr(result, k, v)
        return result


def __query_decorator(func):
    """
    Private method: Call decorator
    :param func:
    :return:
    """
    def run_query(*v):
        logging.info(v[0].__rpc_endpoint__)
        response_object = __remote_call(v[0].__rpc_endpoint__,
                                  v[0].__models_module__,
                                  v[0].__rpc_extras__,
                                  func.__name__, *v)
        #return func(*v)
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
                setattr(cls, attr, __query_decorator(getattr(cls, attr)))
        return cls
    return decorate


def __serialize_object__(obj):
    return json.dumps(obj, default=__object_serializer)


def serializable(original_class):
    """
    Decorator used to declare a serializable model (class level)
    :param original_class:
    :return:
    """
    orig_init = original_class.__init__

    def __init__(self, *args, **kws):
        setattr(original_class, "__serializable__", classmethod(lambda: True))
        setattr(original_class, "response", classmethod(__serialize_object__))
        orig_init(self, *args, **kws)

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
        obj = __object_deserializer(models_module, i)
        params_list.append(obj)
    method_reference = getattr(controller, controller_method)
    return method_reference(*params_list)


def response(obj):
    """
    Format the response compatible with remotipy
    :param obj:
    :return:
    """
    return json.dumps(obj,  default=__object_serializer)