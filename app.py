#!/usr/bin/env python
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
#            (r"/", MainHandler),
            (r"/websocket", ChatSocketHandler),
            (r'/static/(.*)/?', tornado.web.StaticFileHandler, {'path': 'static'}),
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
    cache_size = 200

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
        cls.count += 1
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size :]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        #chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        #chat["html"] = tornado.escape.to_basestring(
        #    self.render_string("message.html", message=chat)
        #)
        message_handlers = {
            'settings': self.handle_settings,
            'message': self.handle_message
        }
        type = parsed['type']
        message_handlers[type](parsed)

    def handle_settings(self, data):
        print('Settings were updated')


    def handle_message(self, data):
        # just reuse data?
        chat = {'type': 'message', 'body': data['body'], 'count': self.count, 'username': data['username']}
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

