import time

from tomato import cmd_ext
from tomato import cmd_origin


class Remote(object):
    """
    远程用户
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
    return cmd_origin.cmd_remote(cmd, username, password, ip, port)


def cmd_remote_args(cmd, username, password, ip, args, finish_match=None, port=22):
    """
    交互式执行远程命令; 注意：只有ubuntu 16测试过.
    :param str cmd: linux cmd
    :param str username: ssh username
    :param str password: ssh password
    :param str ip: ssh host
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :param int port: ssh port
    :return tuple of flag('success','failure'), message
    """
    return cmd_origin.cmd_remote_args(cmd, username, password, ip, args, finish_match, port)


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
    return cmd_origin.cmds_remote(cmds, username, password, ip, port)


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
    return cmd_origin.put_remote(username, password, ip, local_file, remote_file, port)


def cmd_remotes(cmd, remotes):
    """
    执行远程命令
    :param str cmd: linux cmd
    :param list remotes: list for remote object
    :return list of tuple of flag
    """
    return cmd_ext.cmd_remotes(cmd, remotes)


def cmd_remotes_args(cmd, remotes, args, finish_match=None):
    """
    执行远程命令
    :param str cmd: linux cmd
    :param list remotes: remote object
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :return list of tuple of flag
    """
    return cmd_ext.cmd_remotes_args(cmd, remotes, args, finish_match)


def cmds_remotes(cmds, remotes):
    """
    执行远程命令
    :param list cmds: linux cmds
    :param list remotes: list for remote object
    :return list of list of tuple of flag
    """
    return cmd_ext.cmds_remotes(cmds, remotes)


def put_remotes(remotes, local_file, remote_file):
    """
    执行远程复制
    :param list remotes: list for remote object
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    """
    cmd_ext.put_remotes(remotes, local_file, remote_file)


def cmd_remote_args_parallel1(remotes, cmd, args, finish_match, executor):
    """
    交互式执行命令 parallel模式
    :param list remotes: list for remote object
    :param str cmd: linux cmd
    :param list args: cmd args
    :param str or None finish_match: key word flag that cmd finish
    :param executor executor: execute pool
    """
    cmd_ext.cmd_remote_args_parallel1(remotes, cmd, args, finish_match, executor)


def cmd_remote_args_parallel2(remote_cmd_and_args, finish_match, executor):
    """
    交互式执行命令 parallel模式
    :param map remote_cmd_and_args: k:remote - v:list of cmd and args
    :param str or None finish_match: key word flag that cmd finish
    :param executor executor: execute pool
    """
    cmd_ext.cmd_remote_args_parallel2(remote_cmd_and_args, finish_match, executor)


def put_remote_parallel1(remotes, local_file, remote_file, executor):
    """
    执行远程复制 parallel模式
    :param list remotes: remote object
    :param str local_file: local file abs path
    :param str remote_file: remote file abs path
    :param executor executor: execute pool
    """
    cmd_ext.put_remote_parallel1(remotes, local_file, remote_file, executor)


def put_remote_parallel2(remote_to_local_and_remote_file, executor):
    """
    执行远程复制 parallel模式
    :param map remote_to_local_and_remote_file: remote object: k:rmeote - v:[local_file,remote_file]
    :param executor executor: execute pool
    """
    cmd_ext.put_remote_parallel2(remote_to_local_and_remote_file, executor)


def cmds_remote_parallel1(remotes, cmds, executor):
    """
    执行命令 parallel模式
    :param list remotes: remote object
    :param list cmds: linux cmds
    :param executor executor: execute pool
    """
    cmd_ext.cmds_remote_parallel1(remotes, cmds, executor)


def cmds_remote_parallel2(remote_to_cmds, executor):
    """
    执行命令 parallel模式
    :param map remote_to_cmds: k:remote - v:cmds
    :param executor executor: execute pool
    """
    cmd_ext.cmds_remote_parallel2(remote_to_cmds, executor)


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
