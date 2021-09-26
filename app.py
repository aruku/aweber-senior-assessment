from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json

widgets = []

class WidgetsHandler(RequestHandler):
    def get(self):
        self.write({'widgets': widgets})

class WidgetHandler(RequestHandler):
    def post(self):
        widgets.append(json.loads(self.request.body))

def make_app():
    urls = [
        ("/api/widgets/", WidgetsHandler),
        ("/api/widget/", WidgetHandler),
    ]
    return Application(urls, debug=True)

if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()