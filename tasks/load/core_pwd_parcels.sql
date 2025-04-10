DROP TABLE IF EXISTS core.{table_name};

CREATE TABLE core.{table_name} AS
SELECT brt_id AS property_id, *
FROM ${dataset_name}.{table_name};
