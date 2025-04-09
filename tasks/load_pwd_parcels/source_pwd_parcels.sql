CREATE OR REPLACE EXTERNAL TABLE ${dataset_name}.{table_name}(
    `geog` STRING,
    `PARCELID` INTEGER,
    `TENCODE` STRING,
    `ADDRESS` STRING,
    `OWNER1` STRING,
    `OWNER2` STRING,
    `BLDG_CODE` STRING,
    `BLDG_DESC` STRING,
    `BRT_ID` STRING,
    `NUM_BRT` INTEGER,
    `NUM_ACCOUN` INTEGER,
    `GROSS_AREA` INTEGER,
    `PIN` INTEGER,
    `PARCEL_ID` STRING,
    `Shape__Area` FLOAT64,
    `Shape__Length` FLOAT64
)
    OPTIONS(
        format = 'JSON',
        uris = ['gs://${bucket_name}/{prepared_blobname}']
    )
