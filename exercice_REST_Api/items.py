from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import tornado
from tornado.httpserver import HTTPServer
import os
from tornado.options import define, options

items = []
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

class printItems(RequestHandler):
    def get(self):
      if len(items) == 0:
        return self.write("No Item available")
      else:
        return self.render("items.html", items=items)

class TodoItem(RequestHandler):
  def post(self, _):
    # add the item in items
    data  = json.loads(self.request.body)
    print(data)
    items.append(data)
    self.write({'message': 'new item added'})

  def delete(self, id):
    contain = False
    for item in items:
      print(item["id"])
      if item["id"] == int(id):
        contain=True
        items.remove(item)
        self.write({'message': 'Item with id %s was deleted' % id})
    if not contain:
      self.write({'message': 'Item with id %s was not found' % id})


def make_app():
  urls = [
    (r"/", printItems),
    (r"/api/item/([^/]+)?", TodoItem)
  ]
  return Application(urls, 
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=options.debug
    )
  
if __name__ == '__main__':
    app = make_app()
    server = HTTPServer(app)
    server.listen(options.port)
    print("I'm listening on port http://localhost:%i" % options.port)
    tornado.autoreload.start()
    IOLoop.current().start()

