# 搭建rabbitmq docker集群

## 手动搭建
先手动搭建了解rabbitmq集群搭建的流程

## 停止docker rabbitmq

```
docker rm $(docker stop $(docker ps | grep rabbit | awk '{print $1}'))
```

### 设置节点Host
实体机安装需要设置各节点的host到/etc/hosts，rabbitmq加入集群需要

```
172.16.35.12 rabbitmq1
172.16.35.11 rabbitmq2
```

### 启动rabbitmq
先选取3个节点启动rabbitmq docker

node1:

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

node2:

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

### 加入集群

进入rabbitmq2容器

```
docker exec -it rabbitmq2 bash 
```

停止rabbitmq

```
rabbitmqctl stop_app
```

加入集群

```
rabbitmqctl --ram join_cluster rabbit@rabbitmq1
```

出现下面的错误应该是host配置问题，可以先试下是否能ping通

```
rabbit@rabbitmq2:
  * connected to epmd (port 4369) on rabbitmq2
  * epmd reports node 'rabbit' uses port 25672 for inter-node and CLI tool traffic
  * TCP connection succeeded but Erlang distribution failed

  * Node name (or hostname) mismatch: node "rabbit@rabbitmq1" believes its node name is not "rabbit@rabbitmq1" but something else.
    All nodes and CLI tools must refer to node "rabbit@rabbitmq1" using the same name the node itself uses (see its logs to find out what it is)
```

启动rabbitmq

```
rabbitmqctl start_app
```