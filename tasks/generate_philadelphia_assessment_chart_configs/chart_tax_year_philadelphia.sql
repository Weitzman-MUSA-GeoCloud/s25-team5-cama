SELECT
          tax_year,
          lower_bound,
          upper_bound,
          property_count
        FROM
          derived.tax_year_assessment_bins
        ORDER BY lower_bound