# -*- coding: utf-8 -*-

import sys, os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.stack_context import NullContext

from codeMarble_Web import create_app

reload(sys).setdefaultencoding('utf-8')

application = create_app()

if __name__ == '__main__':

    print "fbehdrl123"

    http_server = HTTPServer(WSGIContainer(application))

    try:
        path, _ = os.path.split(os.path.abspath(__file__))
        os.mkdir(os.path.join(path, 'problemData'))

    except Exception as e:
	    pass


    with NullContext():
        http_server.bind(80)
        http_server.start(2)

    IOLoop.instance().start()