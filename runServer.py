# -*- coding: utf-8 -*-

import sys, os
thisPath, _ = os.path.split(os.path.abspath(__file__))

if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from tornado.web import RequestHandler, Application
    from tornado.stack_context import NullContext

    from codeMarble_Web import create_app
    from codeMarble_Web.codeMarble_propertyParser import configs, propertyParser
    propertyParser()

    reload(sys).setdefaultencoding('utf-8')
    application = create_app()


    http_server = HTTPServer(WSGIContainer(application))

    try:
        path, _ = os.path.split(os.path.abspath(__file__))
        os.mkdir(os.path.join(path, 'problemData'))

    except Exception as e:
	    pass


    with NullContext():
        http_server.bind(int(configs['webPort']))
        http_server.start(int(configs['processCount']))

    IOLoop.instance().start()