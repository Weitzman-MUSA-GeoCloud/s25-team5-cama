DROP TABLE IF EXISTS core.{table_name};

CREATE TABLE core.{table_name} AS
SELECT parcel_number AS property_id, *
FROM ${dataset_name}.{table_name};
