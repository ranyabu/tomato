#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    cmd_ext_batch 是基于cmd_ext执行远程命令的扩展类；
        提供ext的批量和并发执行支持
"""
import uuid
from concurrent import futures

from tomato.cmd_exec import *


def cmd_to_batch(remotes, cmd):
    """
    执行远程命令
    :param list remotes: list for remote object
    :param str cmd: linux cmd
    :return list of tuple of flag
    """

    def do(remote):
        return cmd_to(remote, cmd)

    return list(map(do, remotes))


def cmd_to_batch_with_args(remotes, cmd, args, finish_match=None):
    """
    执行远程命令
    :param list remotes: remote object
    :param str cmd: linux cmd
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :return list of tuple of flag
    """

    def do(remote):
        return cmd_to_with_args(remote, cmd, args, finish_match)

    return list(map(do, remotes))


def cmds_to_batch(remotes, cmds, ):
    """
    执行远程命令
    :param list remotes: list for remote object
    :param list cmds: linux cmds
    :return list of list of tuple of flag
    """

    def do(remote):
        return cmds_to(remote, cmds)

    return list(map(do, remotes))


def copy_file_to_batch(remotes, local_file, remote_file):
    """
    执行远程复制
    :param list remotes: list for remote object
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    """
    for remote in remotes:
        copy_file_to(remote, local_file, remote_file)


def cmd_to_batch_with_args_parallel1(remotes, cmd, args, finish_match, executor):
    """
    交互式执行命令 parallel模式
    :param list remotes: list for remote object
    :param str cmd: linux cmd
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remotes:
        f = executor.submit(cmd_to_with_args, remote, cmd, args, finish_match)
        fs.append(f)
        f_all[f] = (remote, cmd, args)
    _print_future(task_id, fs, f_all, f_error)


def cmd_to_batch_with_args_parallel2(remote_cmd_and_args, finish_match, executor):
    """
    交互式执行命令 parallel模式
    :param map remote_cmd_and_args: k:remote - v:list of cmd and args
    :param str or None finish_match: key word flag that cmd finish
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remote_cmd_and_args:
        cmd, args = remote_cmd_and_args[remote]
        f = executor.submit(cmd_to_with_args, remote, cmd, args, finish_match)
        fs.append(f)
        f_all[f] = (remote, cmd, args)
    _print_future(task_id, fs, f_all, f_error)


def copy_file_to_batch_parallel1(remotes, local_file, remote_file, executor):
    """
    执行远程复制 parallel模式
    :param list remotes: remote object
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remotes:
        f = executor.submit(copy_file_to, remote, local_file, remote_file)
        fs.append(f)
        f_all[f] = (remote, local_file, remote_file)
    _print_future(task_id, fs, f_all, f_error)


def copy_file_to_batch_parallel2(remote_to_local_and_remote_file, executor):
    """
    执行远程复制 parallel模式
    :param map remote_to_local_and_remote_file: remote object: k:rmeote - v:[local_file,remote_file]
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remote_to_local_and_remote_file.keys():
        local_file, remote_file = remote_to_local_and_remote_file[remote]
        f = executor.submit(copy_file_to, remote, local_file, remote_file)
        fs.append(f)
        f_all[f] = (remote, local_file, remote_file)
    _print_future(task_id, fs, f_all, f_error)


def cmds_to_batch_parallel1(remotes, cmds, executor):
    """
    执行命令 parallel模式
    :param list remotes: remote object
    :param list cmds: linux cmds
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remotes:
        # print(remote, cmds)
        f = executor.submit(cmds_to, remote, cmds)
        fs.append(f)
        f_all[f] = (remote, cmds)
    _print_future(task_id, fs, f_all, f_error)


def cmds_to_batch_parallel2(remote_to_cmds, executor):
    """
    执行命令 parallel模式
    :param map remote_to_cmds: k:remote - v:cmds
    :param executor executor: execute pool
    """
    task_id = _print_task_id()
    fs, f_all, f_error = [], {}, {}
    for remote in remote_to_cmds.keys():
        cmds = remote_to_cmds[remote]
        # print(remote, cmds)
        f = executor.submit(cmds_to, remote, cmds)
        fs.append(f)
        f_all[f] = (remote, cmds)
    _print_future(task_id, fs, f_all, f_error)


def _print_task_id():
    task_id = uuid.uuid1()
    print('@ 收到任务：', task_id, sep='')
    return task_id


def _print_future(task_id, fs, f_all, f_error):
    for index, f in enumerate(futures.as_completed(fs)):
        if f.result()[0] == 'error':
            f_error[f] = f_all[f]
            print('!! error of', f_all[f])
        f_all.pop(f)
        if index != 0 and index % 50 == 0:
            if f_all:
                print('@ 未执行情况：')
                for key in f_all.keys():
                    print([str(x) for x in f_all[key]])

    print('@ 完成任务：{0} '.format(task_id))
    if f_error:
        print('@ 任务:{0}执行失败如下：'.format(task_id))
        for key in f_error.keys():
            print([str(x) for x in f_error[key]])
