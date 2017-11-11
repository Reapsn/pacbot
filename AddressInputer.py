# -*- coding: utf-8 -*-

class AddressInputer:

    __hasnext = True

    def __init__(self):
        return

    def hasNext(self):
        return self.__hasnext

    def next(self):
        self.__hasnext = False
        return ('31.13.64.1', 443)
