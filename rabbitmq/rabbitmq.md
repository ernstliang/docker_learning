# 搭建rabbitmq docker集群

## 手动搭建
先手动搭建了解rabbitmq集群搭建的流程

### 设置节点Host
实体机安装需要设置各节点的host到/etc/hosts，rabbitmq加入集群需要

```
172.16.35.12 rabbitmq1
172.16.35.11 rabbitmq2
```

### 启动rabbitmq
先选取3个节点启动rabbitmq docker

- node1:

```
-p 5672:5672 \
-p 15672:15672 \
-p 4369:4369 \
-p 25672:25672 \
```

host网络模式启动，不需要指定导出端口

```
docker run -d \
--name=rabbitmq1 \
-e RABBITMQ_NODENAME=rabbit \
-e RABBITMQ_DEFAULT_USER=test \
-e RABBITMQ_DEFAULT_PASS=test \
-e RABBITMQ_ERLANG_COOKIE='0F603647-75B4-4B68-BF13-B801F666932B' \
--add-host=rabbitmq1:172.16.35.12 \
--add-host=rabbitmq2:172.16.35.11 \
--net=host \
-h rabbitmq1 \
rabbitmq:3.7.14-management
```

- node2:

```
docker run -d \
--name=rabbitmq2 \
-e RABBITMQ_NODENAME=rabbit \
-e RABBITMQ_DEFAULT_USER=test \
-e RABBITMQ_DEFAULT_PASS=test \
-e RABBITMQ_ERLANG_COOKIE='0F603647-75B4-4B68-BF13-B801F666932B' \
--add-host=rabbitmq1:172.16.35.12 \
--add-host=rabbitmq2:172.16.35.11 \
--net=host \
-h rabbitmq2 \
rabbitmq:3.7.14-management
```

### 创建集群

- 进入rabbitmq2容器

```
docker exec -it rabbitmq2 bash 
```

- 停止rabbitmq

```
rabbitmqctl stop_app
```

- 加入集群

```
rabbitmqctl --ram join_cluster rabbit@rabbitmq1
```

`--ram`参数表示节点以内存存储方式运行，读写速度快，但重启后数据会丢失，不加`--ram`表示节点以磁盘存储方式运行，读写速度慢，但数据一般可以持久保持。

- 启动rabbitmq

```
rabbitmqctl start_app
```

注: 增加新节点同样操作

### 加入集群的错误

出现下面的错误应该是host配置问题，可以先试下是否能ping通

```
rabbit@rabbitmq2:
  * connected to epmd (port 4369) on rabbitmq2
  * epmd reports node 'rabbit' uses port 25672 for inter-node and CLI tool traffic
  * TCP connection succeeded but Erlang distribution failed

  * Node name (or hostname) mismatch: node "rabbit@rabbitmq1" believes its node name is not "rabbit@rabbitmq1" but something else.
    All nodes and CLI tools must refer to node "rabbit@rabbitmq1" using the same name the node itself uses (see its logs to find out what it is)
```

### 设置镜像队列

在同一个rabbitmq集群中，节点之间并没有主从之分，所有节点会同步相同的队列结构，但队列里的消息并不会同步，不过消息会在节点间传递。这样可用性是比较低的，因为某个节点宕机后，这个节点上的消息不可用，而在其他节点上也没有这些消息的备份，若是该节点无法恢复，则这些消息就丢失了。<br>
为了解决这个问题，可以开启rabbitmq的镜像队列功能，命令如下:

```
rabbitmqctl set_policy ha-all "^" '{"ha-mode":"all"}'
```

- "^"表示所有队列，即所有队列在各个节点上都会有备份。<br>
- 只需在一个节点上设置这个功能，操作会同步到其他节点

详见`参考资料3`

### 手动停止并删除docker rabbitmq

```
docker rm $(docker stop $(docker ps | grep rabbit | awk '{print $1}'))
```

## docker swarm部署rabbitmq集群
TODO

## k8s部署rabbitmq集群
TODO

## 生产环境不适用的策略

### 1. vhost
在生产环境中，如果rabbitmq只为单个系统提供服务的时候，我们适用默认的(/)是可以的。但在为多个系统提供服务时，建议适用单独的vhost。

### 2.user
在生产环境中，删除默认用户(guest)，并设置默认用户只能从localhost链接。
可以创建指定权限的单独用户为每个应用提供服务。对于开启权限的用户，可以使用证书，和源ip地址过滤，和身份验证等方式来加强安全性。

### 3.最大打开文件限制
生产环境中，可能需要调整一些系统的默认限制，以便处理大量的并非连接和队列。需要调整的值有打开的最大文件数。为rabbitmq运行的用户设定65536，对于大多数开发环境来说，4096就已经足够了。

查看默认的打开文件的最大数量

```
ulimit -n
```

更改方式：

- 临时修改

```
ulimit -n 65536
```

- 永久修改

更改配置文件:`/etc/security/limits.conf`
在文件末尾前面加入

```
rabbitmq(启动的用户名)         -       nofile          65536
```

如果更改前用户已经登录的话，需要重新登录下才能生效。

### 4.内存
当rabbitmq检测到它使用的内存超过系统的40%，它将不会再接受任何新的消息，这个值是由参数`vm_memory_high_watermark`来控制的，默认值是一个安全的值，修改该值需要注意。 rabbitmq 的至少需要`128MB`,建议`vm_memory_high_watermark`值为`0.4~0.66` ，不要使用大于`0.7`的值。

### 5.磁盘
磁盘默认的储存数据阈值是50MB，当低于该值的时候，将触发流量限制。<br>
50MB `只适用于开发环境`，生产环境需要调高该值，不然容易由磁盘空间不足导致节点故障，也可能导致数据丢失。<br>
在生产环境中<br>
- 建议的最小值 `{disk_free_limit, {mem_relative, 1.0}}`
它是基于mem_relative的值，例如在具有4GB内存的rabbitmq主机上，那么该磁盘的阈值就是4G，如果磁盘可用空间低于4G，所有生产者和消息都将拒绝。在允许恢复发布之前，通常需要消费者将队列消息消费完。<br>
- 建议的更安全值 `{disk_free_limit, {mem_relative, 1.5}}`
在具有4GB内存的RabbitMQ节点上，如果可用磁盘空间低于6GB，则所有新消息都将被阻止，但是如果我们在停止的时候rabbitmq需要储存4GB的数据到磁盘，再下一次启动的时候，就只有2G空间了。<br>
- 建议的最大值 `{disk_free_limit, {mem_relative, 2.0}}`
这个是最安全的值，如果你的磁盘有足够多的空间话，建议设置该值。但该值容易触发警告，因为在具有4GB内存的rabbitmq主机上，需要最低空间大于8G，如果你的磁盘空间比较少的话，不建议设置该值。

### 6.连接
少使用短连接，使用连接池或者长连接

### 7.TLS
建议尽可能使用TLS连接，使用TLS会对传输的数据加密，但是对系统的吞吐量产生很大的影响

### 8.更改默认端口
常用的web界面的端口`15672`和AMQP 0-9-1 协议端口`5672` ，建议更改，web界面更改，配置参数`management.listener.port`，AMQP 0-9-1 协议端口配置参数 `listeners.tcp.default`。

## 参考资料
- https://www.cnblogs.com/operationhome/p/10483840.html
- https://blog.breezelin.cn/practice-rabbitmq-ha-docker-compose.html
- http://www.cnblogs.com/flat_peach/archive/2013/04/07/3004008.html