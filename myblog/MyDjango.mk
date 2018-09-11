# MyDjango

### 创建密码
因为django的密码是经过哈希的，所以创建时填写的密码也需要是哈希字符串<br>
通过命令./manage.py loaddata superuser.json

```
生成密码:helloword 的哈希
进入django shell
./manage.py shell

>>> from django.contrib.auth.hashers import make_password
>>> make_password('helloword')
'pbkdf2_sha256$120000$tQwFO80tG450$uisyZYrTp03dE4wkQV4+9hm10cLaF1+4d9FFE1dczJ0='
```