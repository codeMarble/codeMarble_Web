# -*- coding: utf-8 -*-

from py3Des.pyDes import triple_des, ECB, PAD_PKCS5
from resource.otherResources import OtherResources

class TripleDES:

    __triple_des = None

    @staticmethod
    def init():
        TripleDES.__triple_des = triple_des(OtherResources().const.TRIPLE_DES_KEY,
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