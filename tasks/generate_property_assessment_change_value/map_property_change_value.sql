WITH base_data AS (
  SELECT
    property_id,
    MAX(market_value_2025) AS market_value_2025,
    MAX(CASE WHEN tax_year = 2024 THEN market_value END) AS market_value_2024,
    ANY_VALUE(neighborhood) AS neighborhood,
    ANY_VALUE(property_address) AS property_address,
    ANY_VALUE(property_geog) AS property_geog
  FROM
    derived.historic_year_property_assessment
  GROUP BY
    property_id
)
SELECT
  property_id,
  neighborhood,
  property_address,
  property_geog,
  market_value_2024,
  market_value_2025,
  (market_value_2025 - market_value_2024) AS change_absolute,
  ROUND(
    SAFE_DIVIDE((market_value_2025 - market_value_2024), market_value_2024),
    2
  ) AS change_percent,
  CASE
    WHEN (market_value_2025 - market_value_2024) > 0 THEN 'increase'
    WHEN (market_value_2025 - market_value_2024) = 0 THEN 'no_change'
    WHEN (market_value_2025 - market_value_2024) < 0 THEN 'decrease'
    ELSE NULL
  END AS change_type
FROM
  base_data
ORDER BY
  property_id
