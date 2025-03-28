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

*load_opa_properties:*
```shell
cd ../load_opa_properties

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
cd ../load_opa_assessments

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
cd ../load_pwd_parcels

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

*the whole workflow:*
```shell
gcloud workflows deploy data-pipeline \
--source=data-pipeline.yaml \
--service-account='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com'

gcloud scheduler jobs create http data-pipeline \
--schedule='0 0 * * 1' \
--time-zone='America/New_York' \
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa5090s25-team5/locations/us-east4/workflows/data-pipeline/executions' \
--oauth-service-account-email='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
--oidc-service-account-email='data-pipeline-user@musa5090s25-team5.iam.gserviceaccount.com' \
```