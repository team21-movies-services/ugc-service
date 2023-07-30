CREATE DATABASE IF NOT EXISTS shard ON CLUSTER company_cluster;

CREATE TABLE IF NOT EXISTS shard.views ON CLUSTER company_cluster (
  id UUID,
  film_id UUID,
  user_id UUID,
  viewed_frame UInt16,
  event_time DATETIME) ENGINE ReplicatedMergeTree (
  '/clickhouse/tables/{shard}',
  '{replica}'
)
PARTITION BY toYYYYMMDD (event_time)
ORDER BY
  event_time;

CREATE TABLE IF NOT EXISTS default.views (
  id UUID,
  film_id UUID,
  user_id UUID,
  viewed_frame UInt16,
  event_time DATETIME) ENGINE Distributed (
  'company_cluster',
  '{database}',
  views,
  rand ());
