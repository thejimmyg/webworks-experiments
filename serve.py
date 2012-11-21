from wsgiref.simple_server import make_server

def app(environ,  start_response):
    start_response('200 OK', [])
    return [b"Hello my lovely lovely Claire!"]

httpd = make_server('', 8000, app)
httpd.handle_request()

#httpd.serve_forever()
