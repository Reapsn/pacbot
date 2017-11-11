# -*- coding: utf-8 -*-

import socket

import logging
import socks


class Util:

    @staticmethod
    def tcpIsOk(address):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            sk.connect(address)
            return True
        except Exception as e:
            logging.debug("address: {0}, exception: {1}".format(address, str(e)))
            return False

    @staticmethod
    def tcpIsOkByPorxy(address, proxyServer):

        sk = socks.socksocket()
        sk.set_proxy(proxyServer.get('proxy_type'),
                     proxyServer.get('addr'),
                     proxyServer.get('port'),
                     proxyServer.get('rdns'),
                     proxyServer.get('username'),
                     proxyServer.get('password'))
        sk.settimeout(1)
        try:
            sk.connect(address)
            return True
        except Exception as e:
            logging.debug("address: {0}, proxyServer: {1}, exception: {2}".format(address, proxyServer, e))
            return False


