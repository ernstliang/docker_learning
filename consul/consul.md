# consul集群搭建

### 创建consul集群docker的本地目录

### 基于centos创建consul的docker镜像

下载consul: https://releases.hashicorp.com/consul/1.2.2/consul_1.2.2_linux_amd64.zip<br>
将下载好的consul可执行程序拷贝到centos的/usr/bin目录下<br>
Dockerfile:
```
FROM centos:latest

ADD . /data
WORKDIR /data

COPY ./consul /usr/bin/
```
编译: 在Dockerfile目录下执行生成docker的镜像
```
docker build -t centos_consul:1.1 .
```

### docker-compose启动consul的docker集群
docker-compose.yml是consul docker集群的配置文件
```
docker-compose up
```
docker集群中映射的Volumes需要执行make_env.sh创建，一个容器一个存储数据的目录，用于数据的持久化

### consul config
```
docker-compose.yml自定义了一个network: consul_net 网段地址: 10.11.0.0
consul集群的机器都部署在同个网段？(尝试下不同的网段？)
server.json
{
    "data_dir": "/data/server1/data",
    "datacenter": "dc1",
    "log_level": "INFO",
    "node_name": "server1",
    "server": true,
    "bind_addr": "172.17.0.100",
    "bootstrap": true,
    "retry_join": ["172.17.0.100", "172.17.0.101", "172.17.0.102"]
}

agent.json
{
    "bind_addr": "10.11.1.13",
    "datacenter": "dc1",
    "data_dir": "/data/agent1/data",
    "log_level": "INFO",
    "node_name": "agent1",
    "server": false,
    "rejoin_after_leave": true,
    "retry_join": ["172.17.0.100", "172.17.0.101", "172.17.0.102"]
}
```

### 启动测试用的docker
```
启动docker
docker run -idt --net consul_consul_net --name agent_consul -v `pwd`:/data/ centos_consul /bin/bash

docker exec -it agent_consul bash

启动consul加入到集群（测试）
consul agent -config-file=./agent2/agent.json &

注册服务
curl -H 'Host: 127.0.0.1:8500' -H 'User-Agent: python-requests/2.18.4' -H 'Accept: */*' --data-binary '{"name": "CrowdFlowCount", "id": "CrowdFlowCount_1111", "address": "10.11.0.2", "port": 38083}' -X PUT --compressed 'http://localhost:8500/v1/agent/service/register'

查询服务
curl 

下载docker容器
docker pull consul:latest
docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' consul agent -server -bind=<external ip> -retry-join=<root agent ip> -bootstrap-expect=<number of server agents> -data-dir=/consul/data -node=<node_name> -client=<client ip> -ui
```
## 问题
1. 启动consul docker集群后web ui一直无法访问，提示8500端口拒绝访问
