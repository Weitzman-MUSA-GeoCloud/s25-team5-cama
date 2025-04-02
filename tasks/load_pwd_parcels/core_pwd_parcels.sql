DROP TABLE IF EXISTS core.pwd_parcels;

CREATE TABLE core.pwd_parcels AS
SELECT brt_id AS property_id, *
FROM source.pwd_parcels;
