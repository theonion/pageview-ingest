CREATE TABLE IF NOT EXISTS ingest.theonion_pageviews (
  path    VARCHAR (512) NOT NULL,
  stamp   TIMESTAMP NOT NULL,
  value   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.avclub_pageviews (
  path    VARCHAR (512) NOT NULL,
  stamp   TIMESTAMP NOT NULL,
  value   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.clickhole_pageviews (
  path    VARCHAR (512) NOT NULL,
  stamp   TIMESTAMP NOT NULL,
  value   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.onionstudios_pageviews (
  path    VARCHAR (512) NOT NULL,
  stamp   TIMESTAMP NOT NULL,
  value   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.starwipe_pageviews (
  path    VARCHAR (512) NOT NULL,
  stamp   TIMESTAMP NOT NULL,
  value   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.theonion_trends (
  content_id  INTEGER NOT NULL,
  stamp       TIMESTAMP NOT NULL,
  value       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.avclub_trends (
  content_id  INTEGER NOT NULL,
  stamp       TIMESTAMP NOT NULL,
  value       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.clickhole_trends (
  content_id  INTEGER NOT NULL,
  stamp       TIMESTAMP NOT NULL,
  value       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.onionstudios_trends (
  content_id  INTEGER NOT NULL,
  stamp       TIMESTAMP NOT NULL,
  value       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingest.starwipe_trends (
  content_id  INTEGER NOT NULL,
  stamp       TIMESTAMP NOT NULL,
  value       INTEGER NOT NULL
);
