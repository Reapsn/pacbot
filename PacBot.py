# -*- coding: utf-8 -*-
import logging.config
import subprocess

import socks

from AddressInputer import AddressInputer
from Util import Util

class PacBot:
    __adressInputer = None
    __directIps = set()
    __proxyIps = set()
    __noWayIps = set()
    proxyServers = list()

    def __init__(self):
        self.__adressInputer = AddressInputer()

    def run(self):
        while (self.__adressInputer.hasNext()):

            address = self.__adressInputer.next()

            if (len(address) != 2):
                logging.error("invalid address: {0}".format(address))
                continue

            if (self.__directIps.__contains__(address[0])):
                continue

            if (self.__proxyIps.__contains__(address[0])):
                continue

            if (self.__noWayIps.__contains__(address[0])):
                continue

            if (Util.tcpIsOk(address)):
                self.__directIps.add(address.host)
                continue

            proxyServer = self.__matchProxyServer(address)
            if (proxyServer):
                self.addToOSPAC(address, proxyServer)
                self.__proxyIps.add(address[0])
            else:
                logging.warn("no way to address: {0}".format(address[0]))
                self.__noWayIps.add(address[0])


    def __matchProxyServer(self, address):

        for proxyServer in self.proxyServers :
            if (Util.tcpIsOkByPorxy(address, proxyServer)):
                return proxyServer

        return None

    def addToOSPAC(self, address, proxyServer):
        cmd = "iptables -t nat -I PREROUTING -p ALL -d {0} -j DNAT --to {1}:{2}".format(address[0], proxyServer.get('addr'), proxyServer.get('port'))
        subprocess.call(cmd)

if __name__ == '__main__':

    logging.config.fileConfig('logging.conf')

    bot = PacBot()

    bot.proxyServers.append({'proxy_type': socks.SOCKS5, 'addr': '127.0.0.1', 'port': 1080})

    bot.run()
