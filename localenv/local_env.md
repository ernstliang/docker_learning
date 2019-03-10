# ASM本地环境搭建
包括mysql、redis、rabbit、trace<br>
通过docker-compose启动

## 使用env定义环境变量供docker-compose使用
创建文件`.env`

```
ENV_MYSQL_PASSWORD=xxxx
ENV_MYSQL_VOLUME=xxxx
ENV_REDIS_PASSWORD=xxxx
ENV_RABBITMQ_NAME=xxx
ENV_RABBITMQ_PASSWORD=xxx
```

## mysql
选择mysql5.7镜像，映射本地volume<br>
docker-compose配置设置默认密码

```
# 环境变量
    environment:
      # mysql密码
      - MYSQL_ROOT_PASSWORD=${ENV_MYSQL_PASSWORD}
```

登陆docker镜像中的mysql

```
$ docker exec -it localenv_mysql_1 bash

登陆mysql
# mysql -uroot -p
输入密码:
```

### 授权其他机器登陆

查看登陆权限

```
mysql> show grants;
+---------------------------------------------------------------------+
| Grants for root@localhost                                           |
+---------------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION |
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION        |
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

设置其他机器的登陆权限

```
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'yourpassword' WITH GRANT OPTION;
```

`注`:yourpassword需要修改成数据库的密码

刷新

```
mysql> FLUSH  PRIVILEGES;
```


### mysql读取配置文件的顺序

```
$ mysqld --help --verbose | grep -A1 -B1 cnf
Default options are read from the following files in the given order:
/etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
The following groups are read: mysqld server mysqld-5.7
--
  -P, --port=#        Port number to use for connection or 0 to default to,
                      my.cnf, $MYSQL_TCP_PORT, /etc/services, built-in default
                      (3306), whatever comes first
```

### 配置本地mysqld.cnf配置文件
通过docker的volume将本地的mysqld.cnf配置文件导入到mysql容器中，具体参考docker-compose.yaml文件<br>
用于修复mysql5.7后版本timestamp设置空是报错的问题

```
volumes:
      - "${ENV_MYSQL_VOLUME}:/var/lib/mysql"
      - "${PWD}/mysql.conf.d:/etc/mysql/mysql.conf.d/"
```

#### 修改mysql配置
设置mysql5.7及以上版本开启了strict模式(严格模式)，timestamp设置为0000-00-00 00:00:00会报错

```
Syntax error or access violation: 1067 Invalid default value for 'xxx'
```

查看sql mode的设置

```
mysql> show variables like "sql_mode";
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

去掉NO_ZERO_IN_DATE和NO_ZERO_DATE可以修复timestamp设置为0000-00-00 00:00:00报错的问题

## 启动trace

jaegertracing/all-in-one数据都存储在内存中所以只能作为测试/联调使用，生产环境不能使用

```
docker run -d --name jaeger   -e COLLECTOR_ZIPKIN_HTTP_PORT=9411   -p 5775:5775/udp   -p 6831:6831/udp   -p 6832:6832/udp   -p 5778:5778   -p 16686:16686   -p 14268:14268   -p 9411:9411   --cpus=1   --memory=512M   jaegertracing/all-in-one:1.9
```