CREATE OR REPLACE EXTERNAL TABLE ${dataset_name}.{table_name}
    OPTIONS(
        format = 'JSON',
        uris = ['gs://${bucket_name}/{prepared_blobname}']
    )
