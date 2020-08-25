# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Remote 远程对象
"""


class Remote(object):
    """
    远程对象
    """

    def __init__(self, username, password, ip, port=22):
        self.__username = username
        self.__password = password
        self.__ip = ip
        self.__port = port

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    def __str__(self, *args, **kwargs):
        return 'Remote (ip=%s, port=%s, username=%s)' % (self.ip, self.port, self.username)
