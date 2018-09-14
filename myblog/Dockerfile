# build python3.6 + gcc
FROM debian_py36:1.0

WORKDIR /data

ADD ./docker-entrypoint.sh /data

EXPOSE 8088
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]