# -*- coding: utf-8 -*-
import json
import logging.config
import subprocess

from AddressInputer import HttpAddressInputer
from Util import Util


class PacBot:
    __adressInputer = None
    __directIps = set()
    __proxyIps = set()
    __noWayIps = set()
    proxyServers = list()

    def __init__(self):
        return

    def run(self):
        while (self.__adressInputer.hasNext()):

            address = self.__adressInputer.next()

            if (len(address) != 2):
                logging.error("invalid address: {0}".format(address))
                continue

            ip, port = address

            if (self.__directIps.__contains__(ip)):
                continue

            if (self.__proxyIps.__contains__(ip)):
                continue

            if (self.__noWayIps.__contains__(ip)):
                continue

            if (Util.tcpIsOk(address)):
                self.__directIps.add(ip)
                continue

            proxyServer = self.__matchProxyServer(address)
            if (proxyServer):
                self.addToOSPAC(address, proxyServer)
                self.__proxyIps.add(ip)
                logging.info("redirect {0}".format(ip))
            else:
                self.__noWayIps.add(ip)
                logging.warn("no way to address: {0}".format(ip))

    def __matchProxyServer(self, address):

        for proxyServer in self.proxyServers:
            if (Util.tcpIsOkByPorxy(address, proxyServer)):
                return proxyServer

        return None

    def addToOSPAC(self, address, proxyServer):

        file = open("clean.sh", "a+")

        try:
            cmd = "iptables -t nat -I PREROUTING -p TCP -d {0} -j DNAT --to {1}:{2}".format(address[0],
                                                                                            proxyServer.get(
                                                                                                'transparent_addr'),
                                                                                            proxyServer.get(
                                                                                                'transparent_port'))
            logging.debug("call '{0}'".format(cmd))
            file.write(cmd.replace("-I", "-D") + "\n")
            subprocess.call(cmd, shell=True)

        finally:
            file.close()

    def config(self, config_json_file):

        jsonfile = open(config_json_file)
        json_config = json.load(jsonfile)

        for proxyServer in json_config["proxyServers"]:
            self.proxyServers.append(proxyServer)

        inputer_config = json_config["inputer"]
        self.__adressInputer = HttpAddressInputer((inputer_config["addr"], inputer_config["port"]))

        jsonfile.close()


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')

    bot = PacBot()

    bot.config("config.json")

    bot.run()
