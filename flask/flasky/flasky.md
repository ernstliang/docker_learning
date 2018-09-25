# Flasky项目说明

## 目录结构
- Flask程序一般都保存在名为app的目录下
- migrations包含数据库迁移脚本
- tests包含单元测试用例
- venv包含运行的虚拟环境
- requirements.txt列出所有依赖包
- config.py存储配置
- manage.py用于启动程序及其他任务


## 数据库迁移
- 创建数据迁移仓库
```
$ python manage.py db init
创建migrations目录
```
- migrate子命令来自动创建迁移脚本
```
$ python manage.py db migrate -m "initial migration"
```
- 更新数据库
```
$ python manage.py db upgrade
```

## css文件位置
项目使用docker启动，分为nginx_flask + myflask，myflask返回的页面中使用了css，但页面调用的css是nginx的static目录下查找到，所以需要在nginx的配置中配置static目录下的css
```
nginx.conf中
location /static {
    alias /data/flasky/www/static;
}
docker-compose.yml指定磁盘映射
volumes:
    - "$PWD/flasky/nginx/conf.d:/etc/nginx/conf.d"
    - "$PWD/flasky/www:/data/flasky/www"
```

## 测试
coverage测试指令
```
$ python manage.py test --coverage
```