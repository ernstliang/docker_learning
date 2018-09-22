# docker版本

- **env_py36 1.0**:
```
docker build -t env_py36:1.0 .

基于python:3.6.6-slim-jessie
安装gcc、g++编译环境

python三方库
uwsgi
django
grpcio
grpcio-tools
googleapis-common-protos
redis
celery
flask
sqlalchemy
mysql-connector-python
pymysql
```