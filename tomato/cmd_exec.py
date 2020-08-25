#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    cmd_exec 是基于paramiko执行远程命令的基础类；
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


def cmd_to(remote, cmd):
    """
    执行远程命令
    :param Remote remote: ssh object
    :param str cmd: linux cmd
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote.ip, remote.port, remote.username, remote.password, timeout=SSH_TIMEOUT)
            print('** TOMATO%s! %s ready   exec:%s' % (task_id, remote.ip + ':' + str(remote.port), cmd))
            _, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read()
            print('** TOMATO%s! %s success exec:%s' % (task_id, remote.ip + ':' + str(remote.port), cmd))
            return 'success', str(result, encoding="utf-8")
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, remote.ip + ':' + str(remote.port), cmd))
            return 'failure', str(e)


def cmd_to_with_args(remote, cmd, args, finish_match=None):
    """
    交互式执行远程命令; 注意：只有ubuntu 16测试过.
    :param Remote remote: ssh object
    :param str cmd: linux cmd
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote.ip, remote.port, remote.username, remote.password, timeout=SSH_TIMEOUT)
            with ssh.invoke_shell() as chan:
                print('** TOMATO%s! %s ready   exec:%s' % (task_id, remote.ip + ":" + str(remote.port), cmd))
                chan.send(cmd + '\n')
                time.sleep(WAIT_TIME)
                s = str(chan.recv(65536), encoding='utf8')
                print(s[s.index('{0}@'.format(remote.username))::])
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
                                                                               remote.ip + ':' + str(remote.port), cmd))
                                    return 'success', out
                                time.sleep(WAIT_TIME)
                                out = str(chan.recv(65536), encoding='utf8')
                        else:
                            print('** TOMATO%s! %s success exec:%s' % (task_id,
                                                                       remote.ip + ':' + str(remote.port), cmd))
                            return 'success', out
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, remote.ip + ':' + str(remote.port), cmd))
            return 'failure', str(e)


def cmds_to(remote, cmds):
    """
    执行远程命令
    :param Remote remote: ssh object
    :param list cmds: cmd list
    :return list of tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    with paramiko.SSHClient() as ssh:
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote.ip, remote.port, remote.username, remote.password, timeout=SSH_TIMEOUT)
            out = []
            for cmd in cmds:
                print('** TOMATO%s! %s ready   exec:%s' % (task_id, remote.ip + ":" + str(remote.port), cmd))
                stdin, stdout, stderr = ssh.exec_command(cmd)
                out.append(str(stdout.read(), encoding="utf-8"))
                print('** TOMATO%s! %s success exec:%s' % (task_id, remote.ip + ':' + str(remote.port), cmd))
            return 'success', out
        except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
            print('** TOMATO%s! %s failure exec:%s' % (task_id, remote.ip + ':' + str(remote.port),
                                                       ''.join(cmds)))
            return 'failure', str(e)


def copy_file_to(remote, local_file, remote_file):
    """
    执行远程复制
    :param Remote remote: ssh object
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    :return tuple of flag('success','failure'), message
    """
    task_id = next(task_counter)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote.ip, remote.port, remote.username, remote.password, timeout=SSH_TIMEOUT)
        paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        print('** TOMATO%s! %s' % (task_id, '开始复制数据,请勿打断程序.'))
        print('** TOMATO%s! %s' % (
            task_id, '复制数据信息:{0}到{1}:{2}{3}'.format(local_file, remote.ip, remote.port, remote_file)))
        start_t = time.time()
        sftp.put(local_file, remote_file)
        temp = '复制数据完成:{0}到{1}:{2}{3},耗时{4}!'.format(local_file, remote.ip, remote.port, remote_file,
                                                     round(time.time() - start_t, 2))
        print('** TOMATO%s! %s' % (task_id, temp))
        return 'success', ''
    except (BadHostKeyException, AuthenticationException, SSHException, socket.error, Exception) as e:
        print('** TOMATO%s! %s failure exec:%s' % (task_id, remote.ip + ':' + str(remote.port),
                                                   local_file + "->" + remote_file))
        return 'failure', str(e)


def check_finish(check_func, not_finish):
    """
    阻塞检查命令是否完成
    :param func check_func: check func which accept element of not_finish
    :param list not_finish: list of element
    :return:
    """
    while len(not_finish) > 0:
        for index in range(len(not_finish) - 1, -1, -1):
            if check_func(not_finish[index]):
                del not_finish[index]
        print('检测尚未执行完毕节点：', list(str(x) for x in not_finish))
        time.sleep(2)
