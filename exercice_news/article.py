#!/usr/bin/env python3

#9e1d0b0198fa42f8b8966332df05b8ed
import asyncio
import tornado.escape
import tornado.ioloop
import tornado.locks
import tornado.web
import os.path
import uuid
import urllib
from tornado import gen
from tornado.gen import multi
from tornado import httpclient
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

articles = dict()
url_src = ["https://newsapi.org/v2/top-headlines?sources=google-news-fr&apiKey=9e1d0b0198fa42f8b8966332df05b8ed"]
class MainHandler(tornado.web.RequestHandler): 
    async def get(self) : 
        global articles
        reponses = await self.getArticles()
        data = tornado.escape.json_decode(reponses.body)
        articles = data
        self.render("index.html", articles=data['articles'])

    async def getArticles(self): 
        global url_src
        http_client = tornado.httpclient.AsyncHTTPClient()
        reponses = await http_client.fetch(url_src[0])
        return reponses

class ArticleDetailHandler(tornado.web.RequestHandler):
    def get(self, id): 
        
        global articles
        try : 
            art = articles['articles'][int(id)]
            self.render("article.html", image=art['urlToImage'],content=art['content'], title=art['title'], author=art['author'],date=art['publishedAt'], url=art['url'])
            
        except Exception as e : 
            print(e)
            self.write('<a href="/"> Go back home</a>')
        
        
            
        

def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler, articles), 
            (r"/detail/([0-9]+)", ArticleDetailHandler, articles)
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()