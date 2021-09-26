from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

widgets = []

class WidgetsHandler(RequestHandler):
    def get(self):
        self.write({'widgets': widgets})

def make_app():
    urls = [
        ("/api/widgets/", WidgetsHandler),
    ]
    return Application(urls, debug=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()