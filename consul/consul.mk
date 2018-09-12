# consul集群搭建

### 创建consul集群docker的本地目录

### 基于centos创建consul的docker镜像
Dockerfile:
```
FROM centos:latest

ADD . /data
WORKDIR /data

COPY ./consul /usr/bin/
```
编译: 在Dockerfile目录下执行生成docker的镜像
```
docker build -t centos_consul .
```



### 启动docker测试
```
自己编译consul docker容器

docker run -idt --name consul \
					-v `pwd`:/data/ \
					-p 8500:8500 \
					-p 8300:8300 \
					-p 8301:8301 \
					-p 8302:8302 \
					-p 8400:8400 \
					-p 8600:8600 \
					centos_consul /bin/bash

docker exec -it consul bash

启动docker
docker run -idt --net consul_consul_net --name agent_consul -v `pwd`:/data/ centos_consul /bin/bash

下载docker容器
docker pull consul:latest
docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' consul agent -server -bind=<external ip> -retry-join=<root agent ip> -bootstrap-expect=<number of server agents> -data-dir=/consul/data -node=<node_name> -client=<client ip> -ui
```

consul config
```
docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' consul agent -server \
				-bind="172.17.0.1" \
				-retry-join="["172.17.0.1", "172.17.0.2", "172.17.0.3"]" \
				-bootstrap-expect=1 \
				-data-dir="/data/consul_data" \
				-node="server1" \
				-ui
				#-client=<client ip> \

server.json
{
    "data_dir": "/data/consul_data",
    "log_level": "INFO",
    "node_name": "server1",
    "server": true,
    "bind_addr": "172.17.0.3",
    "bootstrap": true,
    "retry_join": ["172.17.0.2", "172.17.0.3", "172.17.0.4"]
}
```