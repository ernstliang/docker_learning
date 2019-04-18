#!/bin/bash

DBS=(
    iam_corp            
    iam_corp_dev        
    iam_corp_test       
    iam_dev             
    iam_gw              
    iam_gw_dev          
    iam_gw_test         
    iam_secret_key      
    iam_secret_key_dev  
    iam_secret_key_test 
    iam_secretkey       
    iam_sso             
    iam_sso_dev         
    iam_sso_test        
    iam_subs            
    iam_test            
    iam_user            
    iam_user_dev        
    iam_user_test       
    iam_verify_code     
    iam_verify_code_dev 
    iam_verify_code_test
)

#数据库账号密码
USERNAME=root
PASSWORD=12345678

MYSQL_CMD="mysql -u${USERNAME} -p${PASSWORD}"
echo ${MYSQL_CMD}

#删除数据库
for DBNAME in "${DBS[@]}";
do
echo "${DBNAME}"
CREATE_DB_SQL="DROP DATABASE IF EXISTS ${DBNAME}"
echo ${CREATE_DB_SQL} | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
    echo "drop database ${DBNAME} failed ..."
    exit 1
fi
done