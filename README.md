### TOMATO 是基于是基于paramiko执行远程命令的工具项目

#### 示例
1, 执行命令获取结果

```python
from tomato import api
result = api.cmd_remote('ls -a /', 'root', 'root', '192.168.0.2')
```

2, 批量执行命令

```python
from tomato import api
result1 = api.cmds_remote(['ls -a /', 'ls -a /tmp'], 'root', 'root', '192.168.0.2')
result2 = api.cmd_remotes('ls -a /',[api.Remote('root', 'root', '192.168.0.2'), api.Remote('root', 'root', '192.168.0.3')])
```

3, 并行执行命令

```python
from concurrent import futures
from tomato import api
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    api.cmd_remote_args_parallel1([api.Remote('root', 'root', '192.168.0.2'), api.Remote('root', 'root', '192.168.0.3')],'sudo passwd', ['XY2ghlmcl', 'XY2ghlmcl'], None, executor)
```