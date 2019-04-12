#!/bin/bash

#centos7环境下安装supervisor
#默认python2.7

#easy_install是setuptools包里带的一个命令，使用easy_install实际上是在调用setuptools来完成安装模块的工作,所以安装setuptools即可。
wget --no-check-certificate https://bootstrap.pypa.io/ez_setup.py -O - | sudo python

#安装supervisror
easy_install supervisor

#生成supervisor配置目录
mkdir -p /etc/supervisord.d/{conf,log}

#生成supervisor配置文件
echo_supervisord_conf > /etc/supervisord.conf

#修改supervisord.conf中include的配置参数
echo "[include]" >> /etc/supervisord.conf
echo "files = /etc/supervisord.d/conf/*.ini" >> /etc/supervisord.conf

#启动supervisor
# supervisord -c /etc/supervisord.conf

#配置supervisor开机自启
cp supervisor.service /lib/systemd/system/
systemctl enable supervisor.service
systemctl daemon-reload