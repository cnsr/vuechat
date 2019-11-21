#!/usr/bin/env python
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import pymongo
import os.path
import random
import string
import json
from collections import Counter
from datetime import datetime

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

admin_pw = '1234'

client = pymongo.MongoClient('localhost', 27017)
db = client['vuechat']

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
#            (r"/", MainHandler),
            (r"/websocket", ChatSocketHandler),
            (r"/upload", UploadHandler),
            (r'/static/(.*)/?', tornado.web.StaticFileHandler, {'path': 'static'}),
            (r'/uploads/(.*)/?', tornado.web.StaticFileHandler, {'path': 'uploads'}),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "front/public"),
            static_path=os.path.join(os.path.dirname(__file__), "front/src"),
            xsrf_cookies=False,
        )
        super(Application, self).__init__(handlers, **settings)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    count = 0
    cache = []
    cache_size = 10
    threads = ['General']
    max_threads = 10

    def __init__(self, application, request, **kwargs):
        self.waiterid = str(uuid.uuid4())
        self.cache = list(db.posts.find({'thread': 'General'}))
        print(len(self.cache))
        latest = list(db.posts.find().sort('count', pymongo.DESCENDING).limit(1))
        self.count = latest[0]['count'] if latest else 0
        for x in self.cache:
            del x['_id']
        self.threads.extend(list(set([msg['thread'] for msg in self.cache if msg['thread'] not in self.threads])))
        super().__init__(application, request, **kwargs)

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        ChatSocketHandler.waiters.add(self)
        self.send_updates({'type': 'count', 'usercount': len(self.waiters)})
        self.write_message({'type': 'cached', 'cache': self.cache})

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)
        self.send_updates({'type': 'count', 'usercount': len(self.waiters)})

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        db.posts.insert_one(chat)
        if not chat.get('thread'):
            chat['thread'] = 'General'
        if chat['thread'] not in cls.threads:
            # delete oldest thread
            oldest = db.posts.find_one_and_delete({'thread': {"$ne": 'General'}}, sort=[('count', 1)])
            cls.threads.remove(oldest['thread'])
            cls.send_updates({'type': 'remove_thread', 'count': oldest['thread']})
            db.posts.delete_many({'thread': oldest['thread']})
        cached = [msg for msg in cls.cache if msg['thread'] == chat['thread']]
        # cached is only counts new posts for some reason
        if len(cached) > cls.cache_size:
            extra = db.posts.find_one_and_delete({'thread': chat['thread']}, sort=[('count', 1)])
            cls.send_updates({'type': 'remove', 'count': extra['count']})
            cls.cache[:] = [msg for msg in cls.cache if msg['count'] != extra['count']]


    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        if chat.get('_id'):
            del chat['_id']
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        message_handlers = {
            'settings': self.handle_settings,
            'message': self.handle_message,
            'thread': self.load_thread,
            'admin': self.handle_admin,
        }
        type = parsed['type']
        message_handlers[type](parsed)

    def handle_settings(self, data):
        print('Settings were updated')


    def load_thread(self, data):
        thread = data['thread']
        print(thread)

    def handle_admin(self, data):
            password = data['password']
            print(password)

    def handle_message(self, data):
        # just reuse data?
        self.count += 1
        now = datetime.now()
        now = now.strftime("%m/%d/%Y, %H:%M:%S")
        chat = {
            'type': 'message',
            'body': data['body'],
            'count': self.count,
            'username': data['username'],
            'uid': self.waiterid,
            'thread': data['thread'],
            'filelink': data['filelink'],
            'original_filename': data['filename'],
            'time': now,
        }
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)


class UploadHandler(tornado.web.RequestHandler):

    def check_origin(self, origin):
        return True

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def post(self):
        print('file?')
        print(self.request)
        file = self.request.files['file'][0]
        original_filename = file['filename']
        extension = os.path.splitext(original_filename)[1]
        filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
        out_adr = 'uploads/' + filename + extension
        output = open(out_adr, 'wb')
        output.write(file['body'])
        self.write(json.dumps({'link': out_adr}))
        self.finish()

    get = post

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

