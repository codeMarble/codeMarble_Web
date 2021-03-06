# -*- coding: utf-8 -*-

from py3Des.pyDes import triple_des, ECB, PAD_PKCS5


class TripleDES:

    __triple_des = None

    @staticmethod
    def init():
        TripleDES.__triple_des = triple_des('1234567812345678',
                                            mode=ECB,
                                            IV = '\0\0\0\0\0\0\0\0',
                                            pad=None,
                                            padmode = PAD_PKCS5)

    @staticmethod
    def encrypt(data):
        return TripleDES.__triple_des.encrypt(data)

    @staticmethod
    def decrypt(data):
        return TripleDES.__triple_des.decrypt(data)