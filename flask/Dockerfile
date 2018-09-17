# 基于env_py36:1.0增加flask三方库
FROM env_py36:1.0

# 扩展flask三方库
ADD ./requirements.txt /data
RUN python -m pip install -r requirements.txt

ADD ./docker-entrypoint.sh /data
WORKDIR /data

EXPOSE 8089
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]