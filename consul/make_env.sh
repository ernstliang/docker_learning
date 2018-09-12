#!/bin/bash

# 解压consul
unzip consul_1.2.2_linux_amd64.zip

# 创建server和agent存储数据的目录
mkdir -p server1/data
mkdir -p server2/data
mkdir -p server3/data
mkdir -p agent1/data
mkdir -p agent2/data