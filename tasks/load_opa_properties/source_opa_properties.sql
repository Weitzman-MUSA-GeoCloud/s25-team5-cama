CREATE OR REPLACE EXTERNAL TABLE ${dataset_name}.{table_name} (
    `objectid` INTEGER,
    `assessment_date` TIMESTAMP,
    `basements` STRING,
    `beginning_point` STRING,
    `book_and_page` STRING,
    `building_code` STRING,
    `building_code_description` STRING,
    `category_code` INTEGER,
    `category_code_description` STRING,
    `census_tract` INTEGER,
    `central_air` STRING,
    `cross_reference` STRING,
    `date_exterior_condition` STRING,
    `depth` FLOAT64,
    `exempt_building` FLOAT64,
    `exempt_land` FLOAT64,
    `exterior_condition` STRING,
    `fireplaces` INTEGER,
    `frontage` FLOAT64,
    `fuel` STRING,
    `garage_spaces` INTEGER,
    `garage_type` INTEGER,
    `general_construction` STRING,
    `geographic_ward` INTEGER,
    `homestead_exemption` INTEGER,
    `house_extension` STRING,
    `house_number` INTEGER,
    `interior_condition` STRING,
    `location` STRING,
    `mailing_address_1` STRING,
    `mailing_address_2` STRING,
    `mailing_care_of` STRING,
    `mailing_city_state` STRING,
    `mailing_street` STRING,
    `mailing_zip` STRING,
    `market_value` FLOAT64,
    `market_value_date` STRING,
    `number_of_bathrooms` INTEGER,
    `number_of_bedrooms` INTEGER,
    `number_of_rooms` INTEGER,
    `number_stories` INTEGER,
    `off_street_open` INTEGER,
    `other_building` STRING,
    `owner_1` STRING,
    `owner_2` STRING,
    `parcel_number` INTEGER,
    `parcel_shape` STRING,
    `quality_grade` STRING,
    `recording_date` TIMESTAMP,
    `registry_number` STRING,
    `sale_date` TIMESTAMP,
    `sale_price` FLOAT64,
    `separate_utilities` STRING,
    `sewer` STRING,
    `site_type` STRING,
    `state_code` STRING,
    `street_code` INTEGER,
    `street_designation` STRING,
    `street_direction` STRING,
    `street_name` STRING,
    `suffix` STRING,
    `taxable_building` FLOAT64,
    `taxable_land` FLOAT64,
    `topography` STRING,
    `total_area` FLOAT64,
    `total_livable_area` FLOAT64,
    `type_heater` STRING,
    `unfinished` STRING,
    `unit` STRING,
    `utility` STRING,
    `view_type` STRING,
    `year_built` INTEGER,
    `year_built_estimate` STRING,
    `zip_code` INTEGER,
    `zoning` STRING,
    `pin` INTEGER,
    `building_code_new` STRING,
    `building_code_description_new` STRING,
    `geog` STRING
)
    OPTIONS(
        format = 'JSON',
        uris = ['gs://${bucket_name}/{prepared_blobname}']
    )
