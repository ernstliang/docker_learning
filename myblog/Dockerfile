FROM python:3.6.6-myself

ADD . /data
WORKDIR /data

#RUN apt-get update >1.txt 2>&1
# RUN apt-get -y install mariadb-devel 
# RUN apt-get -y install redis
# RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple virtualenv
RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r requirements.txt

EXPOSE 80
RUN chmod u+x start_script.sh
ENTRYPOINT [ "./start_script.sh" ]