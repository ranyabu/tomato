### TOMATO 是基于paramiko执行远程命令的工具项目

TOMATO 提供丰富的远程执行命令，可以基于此进行规模性的批量执行工作

#### 示例
1, 执行命令获取结果

```python
from tomato.cmd_exec_batch import *
from tomato.remote import *
remote = Remote('username', 'password', '192.24.45.23')
result = cmd_to(remote, 'ls - a / ')
print(result)
```

2, 批量执行命令

```python
from tomato.cmd_exec_batch import *
from tomato.remote import *
remote = Remote('username', 'password', '192.24.45.23')
result = cmds_to(remote, ['ls -a /', 'ls -a /home/username'])
print(result)
```

3, 并行执行命令
> 并行执行命令的模式下，不返回执行结果

```python
from tomato.cmd_exec_batch import *
from tomato.remote import *
from concurrent import futures
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    cmd_to_batch_with_args_parallel1(
        [Remote('root', 'root', '192.168.0.2'), Remote('root', 'root', '192.168.0.3')], 'sudo passwd',
        ['XY2ghlmcl', 'XY2ghlmcl'], None, executor)
```

4, 阻塞检查命令完成

```python
from concurrent import futures
from tomato.cmd_exec_batch import *
from tomato.remote import *

remotes = [Remote('root', 'root', '192.168.0.2'), Remote('root', 'root', '192.168.0.3')]
copy_file_to_batch(remotes, '/tmp/a.txt', '/tmp/a.txt')


def check_f(remotes):
    _, out = cmd_to_batch(remotes, 'ls -a /tmp')
    if 'a.txt' in out:
        return True
    return False


check_finish(check_f, remotes)
```
