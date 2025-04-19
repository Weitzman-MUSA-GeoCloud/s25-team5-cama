SELECT
  tax_year,
  lower_bound,
  upper_bound,
  property_count,
  neighborhood
FROM
  derived.current_year_neighborhood_assessment_bins
ORDER BY
  neighborhood, lower_bound
