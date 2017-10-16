#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    cmd_origin 是基于paramiko执行远程命令的基础类；
        提供基本执行远程命令，执行远程带交互式命令，复制本地文件到远程
"""
import socket
import time

import paramiko
from paramiko import SSHException, BadHostKeyException, AuthenticationException

SSH_TIMEOUT = 5
WAIT_TIME = 1


def _task_counter(n):
    while True:
        yield n
        n += 1


task_counter = _task_counter(1)


def cmd_remote(cmd, username, password, ip, port=22):
    """
    执行远程命令
    :param str cmd: linux cmd
    :param str username: ssh username
    :param str password: ssh password
    :param str ip: ssh host
    :param int port: ssh port
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=SSH_TIMEOUT)
            print('** TOMATO%s! %s ready   exec:%s' % (task_id, ip + ':' + str(port), cmd))
            _, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            print('** TOMATO%s! %s success exec:%s' % (task_id, ip + ':' + str(port), cmd))
            return 'success', result
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, ip + ':' + str(port), cmd))
            return 'failure', str(e)


def cmd_remote_args(cmd, username, password, ip, args, finish_match=None, port=22):
    """
    交互式执行远程命令; 注意：只有ubuntu 16测试过.
    :param str cmd: linux cmd
    :param str username: ssh username
    :param str password: ssh password
    :param str ip: ssh host
    :param list args: cmd args
    :param str finish_match: key word flag that cmd finish
    :param int port: ssh port
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=SSH_TIMEOUT)
            with ssh.invoke_shell() as chan:
                print('** TOMATO%s! %s ready   exec:%s' % (task_id, ip + ":" + str(port), cmd))
                chan.send(cmd + '\n')
                time.sleep(WAIT_TIME)
                s = str(chan.recv(65536), encoding='utf8')
                print(s[s.index('{0}@'.format(username))::])
                for index, arg in enumerate(args):
                    print('** enter arg {0}'.format(arg))
                    chan.send(arg + '\n')
                    time.sleep(WAIT_TIME)
                    out = str(chan.recv(65536), encoding='utf8')
                    if index != len(args) - 1:
                        print(out)
                    else:
                        if finish_match is not None:
                            while True:
                                if finish_match in out:
                                    time.sleep(WAIT_TIME)
                                    print('** TOMATO%s! %s success exec:%s' % (task_id,
                                                                               ip + ':' + str(port), cmd))
                                    return 'success', out
                                time.sleep(WAIT_TIME)
                                out = str(chan.recv(65536), encoding='utf8')
                        else:
                            print('** TOMATO%s! %s success exec:%s' % (task_id,
                                                                       ip + ':' + str(port), cmd))
                            return 'success', out
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, ip + ':' + str(port), cmd))
            return 'failure', str(e)


def cmds_remote(cmds, username, password, ip, port=22):
    """
    执行远程命令
    :param list cmds: linux cmds
    :param str username: ssh username
    :param str password: ssh password
    :param str ip: ssh host
    :param int port: ssh port
    :return list of tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port, username, password, timeout=SSH_TIMEOUT)
            out = []
            for cmd in cmds:
                print('** TOMATO%s! %s ready   exec:%s' % (task_id, ip + ":" + str(port), cmd))
                stdin, stdout, stderr = ssh.exec_command(cmd)
                out.append(stdout.read())
                print('** TOMATO%s! %s success exec:%s' % (task_id, ip + ':' + str(port), cmd))
            return 'success', out
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, ip + ':' + str(port),
                                                       ''.join(cmds)))
            return 'failure', str(e)


def put_remote(username, password, ip, local_file, remote_file, port=22):
    """
    执行远程复制
    :param str username: ssh username
    :param str password: ssh password
    :param str ip: ssh host
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    :param int port: ssh port
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, password, timeout=SSH_TIMEOUT)
        paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        print('** TOMATO%s! %s' % (task_id, '开始复制数据,请勿打断程序.'))
        print('** TOMATO%s! %s' % (task_id,
                                   '复制数据信息:{0}到{1}:{2}{3}'.format(local_file, ip, port, remote_file)))
        start_t = time.time()
        sftp.put(local_file, remote_file)
        temp = '复制数据完成:{0}到{1}:{2}{3},耗时{4}!'.format(local_file, ip, port, remote_file,
                                                     round(time.time() - start_t, 2))
        print('** TOMATO%s! %s' % (task_id, temp))
        return 'success', ''
    except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
        print('** TOMATO%s! %s failure exec:%s' % (task_id, ip + ':' + str(port),
                                                   local_file + "->" + remote_file))
        return 'failure', str(e)
