DROP TABLE IF EXISTS core.opa_properties;

CREATE TABLE core.opa_properties AS
SELECT parcel_number AS property_id, *
FROM source.opa_properties;
