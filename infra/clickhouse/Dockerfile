FROM clickhouse/clickhouse-server:latest

ARG NODE

COPY ./configs/config.xml /etc/clickhouse-server/config.xml
COPY ./configs/users.xml /etc/clickhouse-server/users.xml
COPY ./configs/${NODE}/* /etc/clickhouse-server/config.d/
COPY ./configs/initial.sql /docker-entrypoint-initdb.d/initial.sql
