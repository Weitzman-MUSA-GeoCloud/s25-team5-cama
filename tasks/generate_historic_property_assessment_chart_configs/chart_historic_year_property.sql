SELECT
  property_id,
  tax_year,
  market_value,
  market_value_2025,
  neighborhood,
  property_address,
  property_geog
FROM
  derived.historic_year_property_assessment
ORDER BY
  property_id, tax_year
