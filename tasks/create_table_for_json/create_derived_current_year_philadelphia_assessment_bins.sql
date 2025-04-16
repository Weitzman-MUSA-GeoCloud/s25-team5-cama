-- Group 2025 property assessments using custom value ranges based on Philly’s housing market and tax policy.
CREATE OR REPLACE TABLE derived.current_year_philadelphia_assessment_bins AS
WITH labeled AS (
  SELECT
    tax_year,
    CASE
      WHEN sale_price_2025 > 0 AND sale_price_2025 <= 100000 THEN 0
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
      WHEN sale_price_2025 > 0 AND sale_price_2025 <= 100000 THEN 100000
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
  FROM derived.current_year_assessment_value
  WHERE sale_price_2025 > 0 AND tax_year = 2025
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
