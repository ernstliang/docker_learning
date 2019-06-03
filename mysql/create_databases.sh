#!/bin/bash
DB=(
    asm_bid_pro
    asm_casemgr
    asm_cms
    asm_collaborative
    asm_cost
    asm_data_statistics
    asm_document
    asm_ecloud
    asm_edu
    asm_order
    asm_product
    asm_provider
    asm_service
    cloud_cms
    dashboard
    falcon_portal
    iam_corp
    iam_customer_service
    iam_gw
    iam_msgcenter
    iam_secret_key
    iam_secretkey
    iam_sso
    iam_user
    iam_verify_code
)

DB_TEST=(
    asm_bid_test
    asm_casemgr_test
    asm_cms_test
    asm_collaborative_test
    asm_collaborative_v2_test
    asm_cost_test
    asm_data_statistics_test
    asm_document_test
    asm_ecloud_test
    asm_edu_test
    asm_order_test
    asm_product_test
    asm_provider_test
    asm_service_test
    iam_corp_test
    iam_customer_service_test
    iam_gw_test
    iam_msgcenter_test
    iam_secret_key_test
    iam_sso_test
    iam_user_test
    iam_verify_code_test
)

DB_DEV=(
    asm_bid_dev
    asm_casemgr_dev
    asm_cms_dev
    asm_collaborative_dev
    asm_cost_dev
    asm_data_statistics_dev
    asm_document_dev
    asm_ecloud_dev
    asm_edu_dev
    asm_order_dev
    asm_product_dev
    asm_provider_dev
    asm_service_dev
    iam_corp_dev
    iam_customer_service_dev
    iam_dev
    iam_gw_dev
    iam_msgcenter_dev
    iam_secret_key_dev
    iam_sso_dev
    iam_user_dev
    iam_verify_code_dev
)

#数据库账号密码
USERNAME=root
PASSWORD=molotest123

MYSQL_CMD="mysql -u${USERNAME} -p${PASSWORD}"
echo ${MYSQL_CMD}

#遍历并创建数据库
for DBNAME in "${DB[@]}";
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