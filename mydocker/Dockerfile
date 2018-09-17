# build python3.6 + gcc
# image: debian_py36:1.1
FROM python:3.6.6-slim-jessie

WORKDIR /data

ADD ./docker-entrypoint.sh /data
ADD ./requirements.txt /data

RUN apt-get update && apt-get install -y build-essential
RUN python -m pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt

EXPOSE 8088
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]