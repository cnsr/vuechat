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
import config

from utils import *

import geoip2.database as gdb
gdbr = gdb.Reader('GeoLite2-City.mmdb')

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

client = pymongo.MongoClient('localhost', 27017)
db = client['vuechat']

with open('front/regioncodes.json') as f:
    regioncodes = json.loads(f.read())

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
#            (r"/", MainHandler),
            (r"/websocket", ChatSocketHandler),
            (r"/upload", UploadHandler),
            (r'/static/(.*)/?', tornado.web.StaticFileHandler, {'path': 'static'}),
            (r'/flags/(.*)/?', tornado.web.StaticFileHandler, {'path': 'flags'}),
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
    ip = None
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
            removeing(oldest)
            cls.threads.remove(oldest['thread'])
            cls.send_updates({'type': 'remove_thread', 'count': oldest['thread']})
            db.posts.delete_many({'thread': oldest['thread']})
        cached = [msg for msg in cls.cache if msg['thread'] == chat['thread']]
        # cached is only counts new posts for some reason
        print('cache oversized', len(cached) > cls.cache_size)
        if len(cached) > cls.cache_size:
            extra = db.posts.find_one_and_delete({'thread': chat['thread']}, sort=[('count', 1)])
            removeing(extra)
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
            'remove': self.handle_remove,
            'ban': self.handle_ban,
        }
        type = parsed['type']
        message_handlers[type](parsed)

    def handle_settings(self, data):
        print('Settings were updated')


    def load_thread(self, data):
        thread = data['thread']
        print(thread)

    def handle_admin(self, data):
        self.write_message({
            'type': 'setadmin',
            'admin': data['password'] == config.ADMIN_PASSWORD
        })

    def handle_message(self, data):
        country = {}
        self.count += 1
        now = datetime.now()
        now = now.strftime("%m/%d/%Y, %H:%M:%S")
        # move ip to init ????
        ip = get_ip(self.request)
        if ip == '127.0.0.1':
            ip = '172.217.20.206'
        gdbr_data = gdbr.city(ip)
        extraflags = ['Bavaria', 'Scotland', 'Wales']
        # exceptions for IPs that are incorrectly detected, has to be changed manually smh
        country['country'] = gdbr_data.country.iso_code
        ip_exceptions = {"80.128.":'Bavaria',
                        "95.91.205": 'Bavaria'}
        is_in_exceptions = [v for k,v in ip_exceptions.items() if ip.startswith(k)]
        if gdbr_data.subdivisions.most_specific.name in extraflags:
            country['country'] = gdbr_data.subdivisions.most_specific.name
            country['countryname'] = country['country']
        elif is_in_exceptions:
            country['country'] = country['countryname'] = is_in_exceptions[0]
        else:
            try:
                country['countryname'] = regioncodes[country['country']]
            except KeyError:
                country['countryname'] = 'Proxy'
                country['country'] = 'PROXY'
        print(country)
        # add city
        country = {'countryname': country['countryname'],
                    'country': country['country'],
                    'long': gdbr_data.location.longitude,
                    'lat': gdbr_data.location.latitude,
                    }
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
            'country': country,
        }
        print('CHAT: ', chat)
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
    
    def handle_remove(self, data):
        if data['admin']:
            extra = db.posts.find_one_and_delete({'count': data['count']})
            self.send_updates({'type': 'remove', 'count': extra['count']})
        else:
            self.write_message({'type': 'error', 'text': 'You are not admin'})

    def handle_ban(self, ban):
        pass


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

