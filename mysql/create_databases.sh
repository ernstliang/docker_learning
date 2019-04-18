#!/bin/bash
Databases=(
    iam_user 
    iam_corp
    iam_sso
    iam_secretkey
    iam_verify_code
    iam_gw
)

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
    asm_bid_dev     
    asm_bid_pro     
    asm_bid_test    
    asm_casemgr     
    asm_casemgr_dev 
    asm_casemgr_test
    asm_collaborativ
    asm_collaborativ
    asm_collaborativ
    asm_collaborativ
    asm_cost        
    asm_cost_dev    
    asm_cost_test   
    asm_cp_dev      
    asm_cp_test     
    asm_document_dev
    asm_document_tes
    asm_ecloud      
    asm_ecloud_dev  
    asm_ecloud_test 
    asm_edu_dev     
    asm_edu_test    
    asm_order       
    asm_order_dev   
    asm_order_test  
    asm_product     
    asm_product_dev 
    asm_product_test
    asm_provider    
    asm_provider_dev
    asm_provider_tes
    asm_service     
    asm_service_dev 
    asm_service_test
)

DBASM=(
    asm_bid_dev     
    asm_bid_pro     
    asm_bid_test    
    asm_casemgr     
    asm_casemgr_dev 
    asm_casemgr_test
    asm_collaborativ
    asm_collaborativ
    asm_collaborativ
    asm_collaborativ
    asm_cost        
    asm_cost_dev    
    asm_cost_test   
    asm_cp_dev      
    asm_cp_test     
    asm_document_dev
    asm_document_tes
    asm_ecloud      
    asm_ecloud_dev  
    asm_ecloud_test 
    asm_edu_dev     
    asm_edu_test    
    asm_order       
    asm_order_dev   
    asm_order_test  
    asm_product     
    asm_product_dev 
    asm_product_test
    asm_provider    
    asm_provider_dev
    asm_provider_tes
    asm_service     
    asm_service_dev 
    asm_service_test
)

#数据库账号密码
USERNAME=root
PASSWORD=molotest123

MYSQL_CMD="mysql -u${USERNAME} -p${PASSWORD}"
echo ${MYSQL_CMD}

#遍历并创建数据库
for DBNAME in "${DBS[@]}";
do
echo "${DBNAME}"
CREATE_DB_SQL="CREATE DATABASE IF NOT EXISTS ${DBNAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci"
echo ${CREATE_DB_SQL} | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
    echo "create database ${DBNAME} failed ..."
    exit 1
fi
done

# mysql -u $USERNAME -p << EOF 2>/dev/null
# CREATE DATABASE iam_mytest CHARACTER SET utf8 collate utf8_general_ci
# EOF