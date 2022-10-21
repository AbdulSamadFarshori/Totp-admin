from werkzeug.wrappers import Request


class Middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        print('path: %s, url: %s' % (request.path, request.url))
        print(environ)
        # if request.path == '/client/add-data':
        #     no_of_rows = ClientData.query.all().count()
        return self.app(environ, start_response)