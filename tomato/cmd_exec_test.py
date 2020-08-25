#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    cmd_exec_test 测试类；
"""
from tomato.cmd_exec_batch import *
from tomato.remote import *

remote = Remote('username', 'password', '192.24.45.23')
result = cmd_to(remote, 'ls - a / ')
print(result)

remote = Remote('username', 'password', '192.24.45.23')
result = cmds_to(remote, ['ls -a /', 'ls -a /home/wls81'])
print(result)

remotes = [Remote('root', 'root', '192.168.0.2'), Remote('root', 'root', '192.168.0.3')]
copy_file_to_batch(remotes, '/tmp/a.txt', '/tmp/a.txt')


def check_f(remotes):
    _, out = cmd_to_batch(remotes, 'ls -a /tmp')
    if 'a.txt' in out:
        return True
    return False


check_finish(check_f, remotes)
