# My flasky
learning flask


## send mail
- MAIL_SERVER: smtp邮箱服务
- MAIL_PORT: smtp邮箱服务使用的端口号，需要根据不同的邮箱服务器确认
- MAIL_USE_SSL: 使用ssl加密方式，需要根据不同的邮箱服务器确认
- MAIL_USERNAME: 发送邮件使用的邮箱账号
- MAIL_PASSWORD: 邮箱开通smtp的三方登陆授权码
- FLASKY_MAIL_SENDER: 需要设置成与发送使用的账号相同


## 使用itsdangerous生成确认令牌
```
$ python manage.py shell
>>> from manage import app
>>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
>>> s = Serializer(app.config['SECRET_KEY'], expires_in = 3600)
>>> token = s.dumps({'confirm': 23})
>>> token
>>> data = s.loads(token)
>>> data
```

## 接入mysql
将myflasky中的数据库从sqlite替换成docker mysql:5.6
### 修改docker-compose.yml
- 新建networks:`flask_net`，子网络:`172.10.0.0/16`
- services下新建mysql，设置mysql固定网络ip:`172.10.0.10`
- 将nginx、flask和mysql都设置到`flask_net`网络下
- 修改flasky配置的db路径，`mysql+mysqlconnector://root:123456@172.10.0.10:3306/myflasky`

### 修改mysql docker支持utf8
- 改flasky配置mysql地址:`mysql+mysqlconnector://root:123456@172.10.0.10:3306/myflasky?charset=utf8`, 增加`charset=utf8`设置
- 修改mysqld.cnf配置文件，增加以下参数配置
```
[mysqld]
character_set_server = utf8mb4
collation-server=utf8mb4_general_ci

[mysql]
default_character_set = utf8mb4

[client]
default_character_set = utf8mb4
```
- 查看数据库编码设置
```
SHOW VARIABLES LIKE 'character_set_%';
SHOW VARIABLES LIKE 'collation_%';
```