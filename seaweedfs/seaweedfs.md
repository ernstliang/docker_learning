# seaweedfs docker-compose

参考网上的docker-compose方法搭建seaweedfs集群发现无法正常启动，

往往会提示以下错误:

```
Only odd number of masters are supported
```
peers的配置

```
-peers=master1:9333,master2:9334,master3:9335
```

多次修改测试后发现，可以使用指定ip替换master1~master3，就能正常启动，原因猜测是seaweedfs是依次启动master节点的，同时指定peers使用的master1~3等并不是传递link地址，而是直接的`master1:9333,master2:9334,master3:9335`导致master节点启动失败

## 指定网路

```
networks:
  weednet:
    driver: bridge
    ipam:
      config:
        - subnet: 172.26.0.0/16
```

subnet自定义一个网段

如果提示错误:

```
user specified IP address is supported only when connecting to networks with user configured subnets
```

可以创建一个subnet

```
docker network create --driver bridge --subnet 172.26.0.0/16 weednet
```

## 指定节点ip

```
networks:
    weednet:
        ipv4_address: 172.26.0.11
```

指定节点ip，ip不能重复

## 启动seaweedfs集群

```
docker-compose -f docker-compose-master.yaml
or
docker-compose -f docker-compose-2.yaml
```