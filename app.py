from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import sqlite3
import datetime
import swagger_ui
from init_swagger import generate_swagger_file

# Initialize components
conn = sqlite3.connect('.widgets.db')
c = conn.cursor()

try:
    c.execute('''CREATE TABLE IF NOT EXISTS widgets (id INTEGER PRIMARY KEY,
        name TEXT, number_parts INT, created TEXT, updated TEXT)''')
except sqlite3.OperationalError as e:
    raise Exception("Can't create the table in the DB: " + str(e))

SWAGGER_API_OUTPUT_FILE = "./swagger.json"


class WidgetsHandler(RequestHandler):
    def get(self):
        c.execute('SELECT * FROM widgets')
        self.finish(json.dumps(c.fetchall()))


class WidgetHandler(RequestHandler):
    def get(self, id: int):
        result = self.getwidgetorfinish(id)
        self.finish(json.dumps(result))

    def getwidgetorfinish(self, id: int):
        c.execute("SELECT * FROM widgets WHERE id=?", [id])
        result = c.fetchone()
        if result is None:
            self.set_status(404)
            self.finish("The ID supplied doesn't exist")
        return result

    def post(self, id: int = 0):
        name, number_parts = self.decodebody()
        self.validate(name, number_parts)

        date_created = datetime.datetime.now()
        c.execute("INSERT INTO widgets (name, number_parts, created) VALUES (?, ?, ?)",
                  (name, number_parts, date_created))
        conn.commit()

    def put(self, id: int):
        self.getwidgetorfinish(id)
        name, number_parts = self.decodebody()
        self.validate(name, number_parts)

        date_updated = datetime.datetime.now()
        c.execute("UPDATE widgets SET name=?, number_parts=?, updated=? WHERE id=?",
                  (name, number_parts, date_updated, id))
        conn.commit()

    def decodebody(self):
        body_decoded = json.loads(self.request.body)
        name = body_decoded["name"]
        number_parts = body_decoded["number_parts"]
        return name, number_parts

    def validate(self, name: str, number_parts: str) -> None:
        if len(name) > 64:
            self.set_status(400)
            self.finish("Name is longer than 64 characters")
        if not isinstance(number_parts, int):
            self.set_status(400)
            self.finish("Number of parts is not an integer")

    def delete(self, id: int):
        self.getwidgetorfinish(id)
        c.execute("DELETE FROM widgets WHERE id=?", [id])
        conn.commit()


def make_app():
    urls = [
        ("/api/widgets/", WidgetsHandler),  # List
        (r"/api/widget/([^/]+)?", WidgetHandler),  # Read, create, update, delete
    ]

    # Initialize Tornado application
    app = Application(urls, debug=True)

    # Generate a fresh Swagger file
    generate_swagger_file(handlers=urls, file_location=SWAGGER_API_OUTPUT_FILE)

    # Start the Swagger UI. Automatically generated swagger.json can also
    # be served using a separate Swagger-service.
    swagger_ui.tornado_api_doc(
        app,
        config_path=SWAGGER_API_OUTPUT_FILE,
        url_prefix="/swagger/spec.html",
        title="Car Brand API",
    )

    return app


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
