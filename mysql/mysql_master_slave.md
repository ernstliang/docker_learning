# mysql主从配置

## 配置主服务器
### 1.修改配置文件

### 2.创建用户

```
CREATE USER 'repl'@'172.17.0.%' IDENTIFIED BY 'E7EJ@#duys';
```

```
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'172.17.0.%' IDENTIFIED BY 'E7EJ@#duys';
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
mysql> change master to master_host='172.17.0.14',master_port=3306,master_user='repl',master_password='E7EJ@#duys',master_log_file='mysql-bin.000006',master_log_pos=154;
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

## 创建数据库账号

### 创建iam账号

```
mysql> GRANT ALL PRIVILEGES ON `iam_%`.* TO 'iam'@'%' identified by 'Mac@87uip#$';
```

错误: 密码不符合当前设置的密码规则
```
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

### 导出iam相关数据库

```
$ mysqldump -u iam -p --default-character-set=utf8 --all-databases > iam.sql
```

### 创建asm账号

```
mysql> GRANT ALL PRIVILEGES ON `asm_%`.* TO 'asm'@'%' identified by 'Cl0udP@ss0rd';
```

### 导出asm相关数据库

```
$ mysqldump -P3306 -uasm -p --default-character-set=utf8 --all-databases > asm.sql
```