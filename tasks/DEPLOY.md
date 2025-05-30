## Deploying instructions

*extract_opa_properties:*
```shell
cd ../extract_opa_properties

gcloud functions deploy extract_opa_properties \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_opa_properties \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=4Gi \
--timeout=240s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_opa_properties --region=us-east4 --project=musa5090s25-team5
```

*extract_opa_assessments:*
```shell
cd ../extract_opa_assessments

gcloud functions deploy extract_opa_assessments \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_opa_assessments \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=4Gi \
--timeout=240s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_opa_assessments --region=us-east4 --project=musa5090s25-team5
```

*extract_pwd_parcels:*
```shell
cd ../extract_pwd_parcels

gcloud functions deploy extract_pwd_parcels \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_pwd_parcels \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=6Gi \
--timeout=560s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_pwd_parcels --region=us-east4 --project=musa5090s25-team5
```

*extract_neighborhoods:*
```shell
cd ../extract_neighborhoods

gcloud functions deploy extract_neighborhoods \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_neighborhoods \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--set-env-vars=DATA_LAKE_BUCKET_PUBLIC=musa5090s25-team5-public \
--memory=4Gi \
--timeout=240s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_neighborhoods --region=us-east4 --project=musa5090s25-team5
```

*extract_landmarks:*
```shell
cd ../extract_landmarks

gcloud functions deploy extract_landmarks \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_landmarks \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_landmarks --region=us-east4 --project=musa5090s25-team5
```

*extract_markets:*
```shell
cd ../extract_markets

gcloud functions deploy extract_markets \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_markets \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_markets --region=us-east4 --project=musa5090s25-team5
```

*extract_crimes:*
```shell
cd ../extract_crimes

gcloud functions deploy extract_crimes \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_crimes \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_crimes --region=us-east4 --project=musa5090s25-team5
```

*extract_311:*
```shell
cd ../extract_311

gcloud functions deploy extract_311 \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=extract_311 \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--memory=3Gi \
--timeout=200s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call extract_311 --region=us-east4 --project=musa5090s25-team5
```

*prepare_opa_properties:*
```shell
cd ../prepare_opa_properties

gcloud functions deploy prepare_opa_properties \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=prepare_opa_properties \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--memory=5Gi \
--timeout=300s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call prepare_opa_properties --region=us-east4 --project=musa5090s25-team5
```

*prepare_opa_assessments:*
```shell
cd ../prepare_opa_assessments

gcloud functions deploy prepare_opa_assessments \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=prepare_opa_assessments \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--memory=8Gi \
--timeout=600s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call prepare_opa_assessments --region=us-east4 --project=musa5090s25-team5
```

*prepare_pwd_parcels:*
```shell
cd ../prepare_pwd_parcels

gcloud functions deploy prepare_pwd_parcels \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=prepare_pwd_parcels \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--memory=8Gi \
--timeout=600s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call prepare_pwd_parcels --region=us-east4 --project=musa5090s25-team5
```

*prepare_neighborhoods:*
```shell
cd ../prepare_neighborhoods

gcloud functions deploy prepare_neighborhoods \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=prepare_neighborhoods \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_RAW=musa5090s25-team5-raw_data \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--memory=4Gi \
--timeout=240s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call prepare_neighborhoods --region=us-east4 --project=musa5090s25-team5
```

*load_opa_properties:*
```shell
cd ../load

gcloud functions deploy load_opa_properties \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=load_opa_properties \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--set-env-vars=DATA_LAKE_DATASET=source \
--memory=1Gi \
--timeout=60s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call load_opa_properties --region=us-east4 --project=musa5090s25-team5
```

*load_opa_assessments:*
```shell
cd ../load

gcloud functions deploy load_opa_assessments \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=load_opa_assessments \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--set-env-vars=DATA_LAKE_DATASET=source \
--memory=1Gi \
--timeout=60s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call load_opa_assessments --region=us-east4 --project=musa5090s25-team5
```

*load_pwd_parcels:*
```shell
cd ../load

gcloud functions deploy load_pwd_parcels \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=load_pwd_parcels \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--set-env-vars=DATA_LAKE_DATASET=source \
--memory=1Gi \
--timeout=60s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call load_pwd_parcels --region=us-east4 --project=musa5090s25-team5
```

*load_neighborhoods:*
```shell
cd ../load

gcloud functions deploy load_neighborhoods \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=load_neighborhoods \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PREPARE=musa5090s25-team5-prepared_data \
--set-env-vars=DATA_LAKE_DATASET=source \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call load_neighborhoods --region=us-east4 --project=musa5090s25-team5
```

*model:*
```shell
cd ../model

gcloud functions deploy model \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=model \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--memory=15Gi \
--timeout=2400s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call model --region=us-east4 --project=musa5090s25-team5
```

*model_to_table:*
```shell
cd ../model_to_table

gcloud functions deploy model_to_table \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=model_to_table \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--memory=2Gi \
--timeout=60s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call model_to_table --region=us-east4 --project=musa5090s25-team5
```

*create_table_for_json:*
```shell
cd ../create_table_for_json

gcloud functions deploy create_table_for_json \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=create_table_for_json \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--memory=4Gi \
--timeout=240s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call create_table_for_json --region=us-east4 --project=musa5090s25-team5
```

*generate_philadelphia_assessment_chart_configs:*
```shell
cd ../generate_philadelphia_assessment_chart_configs

gcloud functions deploy generate_philadelphia_assessment_chart_configs \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=generate_philadelphia_assessment_chart_configs \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PUBLIC=musa5090s25-team5-public \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call generate_philadelphia_assessment_chart_configs --region=us-east4 --project=musa5090s25-team5
```

*generate_neighborhood_assessment_chart_configs:*
```shell
cd ../generate_neighborhood_assessment_chart_configs

gcloud functions deploy generate_neighborhood_assessment_chart_configs \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=generate_neighborhood_assessment_chart_configs \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--set-env-vars=DATA_LAKE_BUCKET_PUBLIC=musa5090s25-team5-public \
--memory=2Gi \
--timeout=120s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call generate_neighborhood_assessment_chart_configs --region=us-east4 --project=musa5090s25-team5
```

*query_historic_property_info:*
```shell
cd ../query_historic_property_info

gcloud builds submit --tag gcr.io/musa5090s25-team5/query-historic-property-info

gcloud run deploy query-historic-property-info \
  --image gcr.io/musa5090s25-team5/query-historic-property-info \
  --project musa5090s25-team5 \
  --region us-east4 \
  --allow-unauthenticated
```

*query_map_property_info:*
```shell
cd ../query_map_property_info

gcloud builds submit --tag gcr.io/musa5090s25-team5/query-map-property-info

gcloud run deploy query-map-property-info \
  --image gcr.io/musa5090s25-team5/query-map-property-info \
  --project musa5090s25-team5 \
  --region us-east4 \
  --allow-unauthenticated
```

*property_tiles_info:*
```shell
cd ../property_tiles_info

gcloud functions deploy property_tiles_info \
--gen2 \
--region=us-east4 \
--runtime=python312 \
--source=. \
--entry-point=property_tiles_info \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--memory=5Gi \
--timeout=300s \
--no-allow-unauthenticated \
--trigger-http

gcloud functions call property_tiles_info --region=us-east4 --project=musa5090s25-team5
```

*the whole workflow:*

Note: use gcloud scheduler jobs create if deploying scheduler for the first time

```shell
gcloud workflows deploy data-pipeline \
--source=data-pipeline.yaml \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--location=us-east4

gcloud scheduler jobs update http data-pipeline \
--schedule='0 0 * * 1' \
--time-zone='America/New_York' \
--location=us-east4 \
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa5090s25-team5/locations/us-east4/workflows/data-pipeline/executions' \
--oauth-service-account-email='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com'
```

*CORS*
```shell
gsutil cors set cors-json-file.json gs://musa5090s25-team5-public
```