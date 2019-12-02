from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import multi
from tornado.httpserver import HTTPServer
import asyncio
import tornado
import os 
import json

define('port', default=8888, help='port to listen on')
urls = ["https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=9e1d0b0198fa42f8b8966332df05b8ed", "https://newsapi.org/v2/top-headlines?sources=google-news-fr&apiKey=9e1d0b0198fa42f8b8966332df05b8ed"]
articles = []


async def update_article(): 
    global articles
    httpclient = AsyncHTTPClient()
    print("Update articles")
    reponse = await multi([httpclient.fetch(url) for url in urls])
    for r in reponse:
        articles += json.loads(r.body)['articles']

class MainHandler(tornado.web.RequestHandler): 
    async def get(self) : 
        global articles
        global urls
        if(len(articles) == 0 ) :
            await update_article()
        #httpclient = AsyncHTTPClient()
        #reponse = await multi([httpclient.fetch(url) for url in urls])
        #for r in reponse:
        #    articles += json.loads(r.body)['articles']
        
        #articles = all_articles['articles']
        self.render("index.html", articles=articles)

class ArticleDetailHandler(tornado.web.RequestHandler) : 
    def get(self, id) :
        global articles 
        id_int = int(id)
        if( id_int < len(articles)): 
            self.render("article.html", article=articles[id_int])
        else : 
            self.write(" <a href='/'> Go back Home </a>")

def make_app():
  urls = [
    (r"/", MainHandler), 
    (r"/article/([0-9]+)", ArticleDetailHandler)
  ]
  return Application(urls, debug=True, template_path=os.path.join(os.path.dirname(__file__),"templates") )
  
if __name__ == '__main__':
    app = make_app()
    http_server = HTTPServer(app)
    http_server.listen(options.port)

    print('Listening on http://localhost:%i' % options.port)
    tornado.ioloop.PeriodicCallback(update_article, 5000).start()
    tornado.ioloop.IOLoop.current().start()

