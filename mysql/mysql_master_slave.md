# mysql主从配置

## 配置主服务器
### 1.修改配置文件

### 2.创建用户

```
create user 'repl'@'172.21.0.%' identified by '12345678';
```

```
grant replication slave on *.* to 'repl'@'172.21.0.%' identified by '12345678';
```

### 3.获取二级制日志的信息


```
mysql> flush tables with read lock;
```

```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      446 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

File的值是当前使用的二进制日志的文件名，Position是该日志里面的位置信息

```
mysql > unlock tables;
```

## 配置从服务器
### 1.修改配置文件

```
[mysqld]

log-bin=mysql-bin
server-id=2
```

### 2.配置同步参数

```
mysql> change master to master_host='172.21.0.10',master_user='repl',master_password='12345678',master_log_file='mysql-bin.000002',master_log_pos=154;
```

启动主从同步进程

```
mysql > start slave;
```

检查状态

```
mysql > show slave status \G
```

两个YES表示配置成功
```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```