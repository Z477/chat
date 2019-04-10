from inspect import isfunction

url_function = {} # {urlxx : {clse:xxx, func:xxx, method:xxx}}

def controller(cls):
    '''
    @summary a Decorator to generate cls's instance
    @param cls: class name
    return: a function to generate class instance
    '''
    for key, value in cls.__dict__.items():
        if isfunction(value) and hasattr(value, 'url_method'):
            url_function[value.url_method['url']] = {'cls' : cls(), 'func' : value, 'method' : value.url_method['method']}
    return cls

def onRequset(url, method):
    def decorator(func):
        func.url_method = {'url':url, 'method':method}
        return func
    return decorator

def application(environ, start_response):

    url = environ.get('PATH_INFO')
    request_method = environ.get('REQUEST_METHOD')

    if url_function.has_key(url) and url_function[url]['method'] == request_method:
        return url_function[url]['func'](url_function[url]['cls'], environ, start_response)
    elif request_method == 'OPTIONS':
        start_response('200 OK', [('Content-Type', 'text/html'),
                                  ('Access-Control-Allow-Origin', '*'),
                                  ('Access-Control-Allow-Methods', 'POST'),
                                  ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')])
        return {}

    else:

        start_response('404', [('Content-Type', 'text/html')])
        return [b'<h1>Not Found!</h1>']



