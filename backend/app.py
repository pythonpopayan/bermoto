# -*- coding: utf-8 -*-

"""

"""

# tornado imports
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado import gen, httpserver
from tornado.options import define, parse_command_line, options

# local imports
from handlers.transactional_messaging import messaging_server

###############################################################################
# GLOBAL VARIABLES
###############################################################################

#define ports input to be set by command line argument
define('port', default=8080, help='port to launch process')

q = {
    'main': Queue()
}

###############################################################################
# MAIN FUNCTION
###############################################################################


@gen.coroutine
def main():
    #get port from commandline
    parse_command_line()
    #create app instance
    # configuration
    port = options.port
    # websockets server
    app = messaging_server(q)
    server = httpserver.HTTPServer(app)
    server.listen(port)
    print(("[app]: Listening on {:}...".format(port)))
    #launch listener server
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
