
from wsgiref.simple_server import make_server
import wsgl
from controller import application

# create a server
httpd = make_server('', 7777, application)
print('Serving HTTP on port 7777...')

# start listening:
httpd.serve_forever()
