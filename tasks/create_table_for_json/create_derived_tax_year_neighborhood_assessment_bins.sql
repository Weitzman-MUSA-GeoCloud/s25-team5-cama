-- Group 2024 property assessments using custom value ranges by neighborhood, based on Philly’s housing market and tax policy.
CREATE OR REPLACE TABLE derived.tax_year_neighborhood_assessment_bins AS
WITH assessments_with_geom AS (
  SELECT
    a.year AS tax_year,
    a.market_value,
    -- 解析 WKT 格式并修正经纬度顺序（原格式为 POINT(lat lon)）
    ST_GEOGPOINT(
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(1)] AS FLOAT64),  -- 经度
      SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(0)] AS FLOAT64)   -- 纬度
    ) AS property_geog
  FROM core.opa_assessments a
  JOIN core.opa_properties p
    ON a.property_id = p.property_id
  WHERE a.market_value > 0 AND a.year = 2024
),
with_neighborhood AS (
  SELECT
    a.tax_year,
    n.name AS neighborhood,
    a.market_value
  FROM assessments_with_geom a
  JOIN core.philly_neighborhoods n
    ON ST_WITHIN(a.property_geog, n.geometry)
),
labeled AS (
  SELECT
    tax_year,
    neighborhood,
    CASE
      WHEN market_value <= 100000 THEN 0
      WHEN market_value <= 200000 THEN 100000
      WHEN market_value <= 300000 THEN 200000
      WHEN market_value <= 400000 THEN 300000
      WHEN market_value <= 600000 THEN 400000
      WHEN market_value <= 800000 THEN 600000
      WHEN market_value <= 1000000 THEN 800000
      WHEN market_value <= 2000000 THEN 1000000
      WHEN market_value <= 5000000 THEN 2000000
      ELSE 5000000
    END AS lower_bound,
    CASE
      WHEN market_value <= 100000 THEN 100000
      WHEN market_value <= 200000 THEN 200000
      WHEN market_value <= 300000 THEN 300000
      WHEN market_value <= 400000 THEN 400000
      WHEN market_value <= 600000 THEN 600000
      WHEN market_value <= 800000 THEN 800000
      WHEN market_value <= 1000000 THEN 1000000
      WHEN market_value <= 2000000 THEN 2000000
      WHEN market_value <= 5000000 THEN 5000000
      ELSE 500000000
    END AS upper_bound
  FROM with_neighborhood
),
aggregated AS (
  SELECT
    tax_year,
    neighborhood,
    lower_bound,
    upper_bound,
    COUNT(*) AS property_count
  FROM labeled
  GROUP BY tax_year, neighborhood, lower_bound, upper_bound
)
SELECT *
FROM aggregated
ORDER BY neighborhood, lower_bound;
