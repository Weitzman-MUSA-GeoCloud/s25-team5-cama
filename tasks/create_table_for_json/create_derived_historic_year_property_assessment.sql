-- Create a historical assessment table for properties with neighborhood, address, and geography
CREATE OR REPLACE TABLE derived.historic_year_property_assessment AS
WITH base_historic AS (
  SELECT
    a.property_id,
    a.year AS tax_year,
    a.market_value,
    p.location AS property_address,
    ST_GEOGPOINT(
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(1)] AS FLOAT64),
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(0)] AS FLOAT64)
    ) AS property_geog
  FROM core.opa_assessments a
  JOIN core.opa_properties p
    ON a.property_id = p.property_id
  WHERE a.market_value > 0 AND a.year BETWEEN 2016 AND 2024 -- Keep 10 years of data (plus 2025)
),
with_neighborhood AS (
  SELECT
    b.property_id,
    b.tax_year,
    b.market_value,
    b.property_address,
    b.property_geog,
    n.name AS neighborhood
  FROM base_historic b
  JOIN core.philly_neighborhoods n
    ON ST_WITHIN(b.property_geog, n.geometry)
),
deduplicated AS (
  -- Keep only one record per property_id and tax_year (highest market_value if duplicates exist)
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY property_id, tax_year ORDER BY market_value DESC) AS rn
  FROM with_neighborhood
),
with_2025 AS (
  -- Join current 2025 assessment data to ensure properties have 2025 values
  SELECT
    d.property_id,
    d.tax_year,
    d.market_value,
    cy.sale_price_2025 AS market_value_2025,
    d.neighborhood,
    d.property_address,
    d.property_geog,
    d.rn
  FROM deduplicated d
  LEFT JOIN derived.current_year_assessment_value cy
    ON d.property_id = cy.property_id AND cy.tax_year = 2025
)
SELECT
  property_id,
  tax_year,
  market_value,
  market_value_2025,
  neighborhood,
  property_address,
  property_geog
FROM with_2025
WHERE rn = 1
  AND market_value_2025 IS NOT NULL  -- Only keep properties that have 2025 data
ORDER BY property_id, tax_year;
