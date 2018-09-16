# 基于debian_py36:1.2增加flask生成1.3版本
FROM debian_py36:1.2

RUN python -m pip install flask

ADD ./docker-entrypoint.sh /data
WORKDIR /data

EXPOSE 8089
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]