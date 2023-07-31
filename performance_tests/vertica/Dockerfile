FROM vertica/vertica-ce:latest

# отключаем генерацию тестовых таблиц vmart
RUN sed -i '/VMART_ETL_SCRIPT/d' /home/dbadmin/docker-entrypoint.sh
