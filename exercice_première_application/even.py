import tornado.autoreload
import os.path
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, RequestHandler

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")
class Even (RequestHandler):
    def get(self):
        n = self.get_argument("n")
        if int(n)%2 == 0:
            res = "Even"
        else:
            res = "Odd"
        return self.render("even.html", res=res, number=n)

if __name__ == "__main__":
    app = Application([
        (r"/", Even)
    ], 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=options.debug
    )
    server = HTTPServer(app)
    server.listen(options.port)
    print("I'm listening on port http://localhost:%i" % options.port)
    tornado.autoreload.start()
    IOLoop.current().start()