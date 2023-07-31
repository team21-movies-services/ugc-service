CREATE DATABASE IF NOT EXISTS shard;

CREATE TABLE IF NOT EXISTS shard.views (
  id UUID DEFAULT generateUUIDv4(),
  film_id UUID,
  user_id UUID,
  viewed_frame UInt16,
  event_time DateTime('UTC'))
    ENGINE ReplicatedMergeTree (
  '/clickhouse/tables/{shard}',
  '{replica}'
)
PARTITION BY toYYYYMMDD (event_time)
ORDER BY
  event_time;

CREATE TABLE IF NOT EXISTS default.views (
  id UUID DEFAULT generateUUIDv4(),
  film_id UUID,
  user_id UUID,
  viewed_frame UInt16,
  event_time DateTime('UTC')) ENGINE Distributed (
  'company_cluster',
  'shard',
  views,
  rand ());
