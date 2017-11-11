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

        file = open("clean.sh", "a")

        try :
            cmd = "iptables -t nat -I PREROUTING -p TCP -d {0} -j DNAT --to {1}:{2}".format(address[0],
                                                                                            proxyServer.get('transparent_addr'),
                                                                                            proxyServer.get('transparent_port'))
            logging.debug("call '{0}'".format(cmd))
            file.write(cmd.replace("-I", "-D"))
            subprocess.call(cmd, shell=True)

            cmd = "iptables -t nat -I PREROUTING -p UDP -d {0} -j DNAT --to {1}:{2}".format(address[0],
                                                                                            proxyServer.get('transparent_addr'),
                                                                                            proxyServer.get('transparent_port'))
            logging.debug("call '{0}'".format(cmd))
            file.write(cmd.replace("-I", "-D"))
            subprocess.call(cmd, shell=True)


        finally:
            file.close()

if __name__ == '__main__':

    logging.config.fileConfig('logging.conf')

    bot = PacBot()

    bot.proxyServers.append({'proxy_type': socks.SOCKS5,
                             'addr': '127.0.0.1',
                             'port': 1080,
                             'transparent_addr':"192.168.3.97",
                             'transparent_port':12345})

    bot.run()
