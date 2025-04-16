-- Group 2025 property assessments using custom value ranges by neighborhood, based on Philly’s housing market and tax policy.
CREATE OR REPLACE TABLE derived.current_year_neighborhood_assessment_bins AS
WITH assessments_with_geom AS (
  SELECT
    a.tax_year,
    a.sale_price_2025,
    -- Convert the property geog from WKT to GEOGRAPHY with correct coordinates
    ST_GEOGPOINT(
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(1)] AS FLOAT64),
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(0)] AS FLOAT64)
    ) AS property_geog
  FROM derived.current_year_assessment_value a
  JOIN core.opa_properties p
    ON a.property_id = p.property_id
  WHERE a.sale_price_2025 > 0 AND a.tax_year = 2025
),
with_neighborhood AS (
  SELECT
    a.tax_year,
    n.name AS neighborhood,
    a.sale_price_2025
  FROM assessments_with_geom a
  JOIN (
    SELECT
      name,
      ST_GEOGFROMGEOJSON(geog) AS geometry
    FROM core.neighborhoods
  ) n
    ON ST_WITHIN(a.property_geog, n.geometry)
),
labeled AS (
  SELECT
    tax_year,
    neighborhood,
    CASE
      WHEN sale_price_2025 <= 100000 THEN 0
      WHEN sale_price_2025 <= 200000 THEN 100000
      WHEN sale_price_2025 <= 300000 THEN 200000
      WHEN sale_price_2025 <= 400000 THEN 300000
      WHEN sale_price_2025 <= 600000 THEN 400000
      WHEN sale_price_2025 <= 800000 THEN 600000
      WHEN sale_price_2025 <= 1000000 THEN 800000
      WHEN sale_price_2025 <= 2000000 THEN 1000000
      WHEN sale_price_2025 <= 5000000 THEN 2000000
      ELSE 5000000
    END AS lower_bound,
    CASE
      WHEN sale_price_2025 <= 100000 THEN 100000
      WHEN sale_price_2025 <= 200000 THEN 200000
      WHEN sale_price_2025 <= 300000 THEN 300000
      WHEN sale_price_2025 <= 400000 THEN 400000
      WHEN sale_price_2025 <= 600000 THEN 600000
      WHEN sale_price_2025 <= 800000 THEN 800000
      WHEN sale_price_2025 <= 1000000 THEN 1000000
      WHEN sale_price_2025 <= 2000000 THEN 2000000
      WHEN sale_price_2025 <= 5000000 THEN 5000000
      ELSE 500000000
    END AS upper_bound
  FROM with_neighborhood
),
aggregated AS (
  SELECT
    tax_year,
    lower_bound,
    upper_bound,
    COUNT(*) AS property_count,
    neighborhood
  FROM labeled
  GROUP BY tax_year, neighborhood, lower_bound, upper_bound
)
SELECT *
FROM aggregated
ORDER BY neighborhood, lower_bound;
