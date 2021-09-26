from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import sqlite3
import datetime

# Initialize components
conn = sqlite3.connect('.widgets.db')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE IF NOT EXISTS widgets (name TEXT, number_parts INT, created TEXT, updated TEXT)''')
except sqlite3.OperationalError as e:
    raise Exception("Can't create the table in the DB: " + str(e))

class WidgetsHandler(RequestHandler):
    def get(self):
        c.execute('SELECT * FROM widgets')
        self.write(json.dumps(c.fetchall()))

class WidgetHandler(RequestHandler):
    def post(self):
        body_decoded = json.loads(self.request.body)
        name = body_decoded["name"]
        number_parts = body_decoded["number_parts"]
        date_created = datetime.datetime.now()
        c.execute("INSERT INTO widgets (name, number_parts, created) VALUES (?, ?, ?)", (name, number_parts, date_created))
        conn.commit()

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