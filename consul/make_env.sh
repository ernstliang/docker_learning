#!/bin/bash

# 下载consul安装包
wget https://releases.hashicorp.com/consul/1.4.3/consul_1.4.3_linux_amd64.zip

# 解压consul
unzip consul_1.4.3_linux_amd64.zip

# 创建server和agent存储数据的目录
mkdir -p server1/data
mkdir -p server2/data
mkdir -p server3/data
mkdir -p agent1/data
mkdir -p agent2/data