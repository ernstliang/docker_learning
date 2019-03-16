# docker启动命令
用于保存一些通用的docker启动命令


## 启动redis
```
docker run -idt --name redis_1 -p 6379:6379 redis
```

## 启动mysql
指定本地映射目录用于数据的持久化
```
docker run -idt --name mysql_1 -p 3306:3306 -v /Users/xliang/Documents/workspace/GitHub/docker/local_data/mysql:/var/lib/mysql --env MYSQL_ROOT_PASSWORD=123456 mysql

-p 导出3306端口到Host主机
-v 指定本地目录的映射, /Users/xliang/Documents/workspace/GitHub/docker/local_data/mysql 到 /var/lib/mysql
--env 通过设置环境变量来设置mysql的root密码
```
