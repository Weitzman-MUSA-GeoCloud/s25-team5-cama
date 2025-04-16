DROP TABLE IF EXISTS core.{table_name};

CREATE TABLE core.{table_name} AS
FROM ${dataset_name}.{table_name};
