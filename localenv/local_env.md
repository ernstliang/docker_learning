# ASM本地环境搭建
包括mysql、redis、rabbit、trace<br>
通过docker-compose启动

## mysql
选择mysql5.7镜像，映射本地volume<br>
docker-compose配置设置默认密码

```
# 环境变量
    environment:
      # mysql密码
      - MYSQL_ROOT_PASSWORD=molotest123
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

刷新

```
mysql> FLUSH  PRIVILEGES;
```


设置mysql5.7及以上版本time等于0报错问题

```
mysql> show variables like "sql_mode";
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| Variable_name | Value                                                                                                                                     |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| sql_mode      | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------------+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```