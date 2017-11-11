# -*- coding: utf-8 -*-
import SocketServer
import logging
import threading
import time
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler


class AddressInputer:
    _hasnext = True

    def __init__(self):
        return

    def hasNext(self):
        return self._hasnext

    def next(self):
        self._hasnext = False
        return ('31.13.64.1', 443)


addresses = list()


class HttpAddressInputer(AddressInputer):
    def __init__(self, addr):
        AddressInputer.__init__(self)

        Handler = MyRequestHandler
        httpd = SocketServer.TCPServer(addr, Handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        logging.info("HttpAddressInputer running on {0}".format(addr))

        return

    def next(self):
        if (len(addresses) > 0):
            return addresses.pop(0)
        else:
            while True:
                if (len(addresses) > 0):
                    return addresses.pop(0)
                else:
                    time.sleep(3)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.process()

    def do_POST(self):

        self.process()

    def process(self):

        if '?' in self.path:

            query = urllib.splitquery(self.path)

            path = query[0]

            queryParams = {}

            for qp in query[1].split('&'):
                kv = qp.split('=')
                if (len(kv) < 2) :
                    continue
                queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')

            try:
                address = (queryParams.get("addr"), int(queryParams.get("port")))
                addresses.append(address)
                self.response("")
            except Exception as e:
                logging.error("get address unsuccessfully, exception: {0}".format(e))
                self.responseHelp()
        else:
            self.responseHelp()


    def responseHelp(self):
        ip, port = self.server.server_address
        self.response("you should request url like this 'http://{0}:{1}/?addr=1.1.1.1&port=11111'".format(ip, port))

    def response(self, message):

        enc = "UTF-8"

        message = message.encode(enc)

        self.send_response(200)

        self.send_header("Content-type", "text/html; charset=%s" % enc)

        self.send_header("Content-Length", str(len(message)))

        self.end_headers()

        self.wfile.write(message)

