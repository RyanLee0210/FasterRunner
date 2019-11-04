#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 15:03
# @Author  : liwaiqiang
# @Site    : AES加密解密--pkcs5
# @File    : crypto_aes.py.py
# @Software: PyCharm
import base64
from Crypto.Cipher import AES
import json
class crypto_aes(object):

    # 此为加密的key
    __key = 'liwaiqiang250e284d1a00liwaiqiang'  # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
    # 此为加密器
    __aes = ''

    def __init__(self):
        self.__aes = AES.new(str.encode(self.__key), AES.MODE_ECB)  # 初始化加密器，本例采用ECB加密模式
    # 补足字符串长度为16的倍数
    def __add_to_16(self,text):
        '''
        :param text:需要调整的文本，string，"{\"account\":\"18823370210\",\"password\":\"Abc1234567\",\"captcha\":\"3534b\"}"
        :return:返回调整后的文本，string
        '''
        while len(text) % 16 != 0:
            text += (16 - len(text) % 16) * chr(16 - len(text) % 16)
        return str.encode(text)  # 返回bytes

    def decrypt_text(self,text):
        '''
        解密函数
        :param text: 已经加密的密文，string，'+KhQ7gOuHKx+pXGGZubK/uih8Gc4/VJ/L4eRwMaIIq7WuPxWRyF12PF+xbz+B1Dfi81dRsL1v3VP0ntLIHx00a5fBHaNcmQfa9QTDfteIrM='
        :return: 返回解密后的明文，string，"{\"account\":\"18823370210\",\"password\":\"Abc1234567\",\"captcha\":\"3534b\"}"
        '''
        decrypted_text = self.__aes.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
        return decrypted_text

    def encrypt_text(self,text):
        '''
        加密函数
        :param text: 需要加密的明文，string，"{\"account\":\"18823370210\",\"password\":\"Abc1234567\",\"captcha\":\"3534b\"}"
        :return: 已经加密的密文，string，'+KhQ7gOuHKx+pXGGZubK/uih8Gc4/VJ/L4eRwMaIIq7WuPxWRyF12PF+xbz+B1Dfi81dRsL1v3VP0ntLIHx00a5fBHaNcmQfa9QTDfteIrM='
        '''
        # 如果text是dict类型数据，先转换成json字符串
        if isinstance(text,dict):
            text = json.dumps(text)
        encrypted_text = str(base64.encodebytes(self.__aes.encrypt(self.__add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
        return encrypted_text
