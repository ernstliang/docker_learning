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

