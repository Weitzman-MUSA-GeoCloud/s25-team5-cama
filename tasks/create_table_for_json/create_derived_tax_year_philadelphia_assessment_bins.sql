-- Group 2024 property assessments using custom value ranges based on Philly’s housing market and tax policy.
CREATE OR REPLACE TABLE derived.tax_year_philadelphia_assessment_bins AS
WITH labeled AS (
  SELECT
    year AS tax_year,
    CASE
      WHEN market_value > 0 AND market_value <= 100000 THEN 0
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
      WHEN market_value > 0 AND market_value <= 100000 THEN 100000
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
  FROM core.opa_assessments
  WHERE market_value > 0 AND year = 2024
),
aggregated AS (
  SELECT
    tax_year,
    lower_bound,
    upper_bound,
    COUNT(*) AS property_count
  FROM labeled
  GROUP BY tax_year, lower_bound, upper_bound
)
SELECT *
FROM aggregated
ORDER BY lower_bound;
