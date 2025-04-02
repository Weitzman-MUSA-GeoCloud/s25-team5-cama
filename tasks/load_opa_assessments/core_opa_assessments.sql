DROP TABLE IF EXISTS core.opa_assessments;

CREATE TABLE core.opa_assessments AS
SELECT parcel_number AS property_id, *
FROM source.opa_assessments;
