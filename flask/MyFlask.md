# my flask demo
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