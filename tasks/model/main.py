import numpy as np
import pandas as lpd
import geopandas as gpd
import json
from shapely.geometry import Point, shape
from datetime import datetime
from sklearn.neighbors import KDTree
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from google.cloud import storage
from google.cloud import bigquery
import io
import functions_framework
import pathlib
import db_dtypes

DATA_DIR = pathlib.Path(__file__).parent


@functions_framework.http
def model(request):

    # Initialize GCS client
    storage_client = storage.Client()
    bucket_name = "musa5090s25-team5-raw_data"

    # Initialize bigquery client
    bigquery_client = bigquery.Client()

    # Function to read CSV from GCS
    def read_csv_from_gcs(bucket_name, file_path, dtype=None):
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        csv_data = blob.download_as_string()
        return lpd.read_csv(io.BytesIO(csv_data), dtype=dtype)

    # Function to read GeoJSON from GCS
    def read_geojson_from_gcs(bucket_name, file_path):
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        geojson_data = blob.download_as_string()
        return gpd.read_file(io.BytesIO(geojson_data))

    print('Extracting 311 and crimes data from raw bucket')

    # Read data from GCS
    requests_311 = read_csv_from_gcs(bucket_name, "311/311.csv", dtype={'zipcode': str})
    crimes2024 = read_csv_from_gcs(bucket_name, "crimes/crimes.csv")

    # Create spatial dataframe
    crimes2024 = gpd.GeoDataFrame(
        crimes2024,
        geometry=gpd.points_from_xy(crimes2024.lng, crimes2024.lat),
        crs='EPSG:4326'
    ).to_crs(epsg=6565)

    homicide = crimes2024[
        crimes2024.iloc[:, 13].isin(['Homicide - Criminal', 'Homicide - Justifiable'])
    ]

    # Filter for thefts
    theft = crimes2024[
        crimes2024.iloc[:, 13].isin(['Thefts', 'Theft from Vehicle'])
    ]

    # Step 1: Filter out rows where 'lat' is NA
    filtered_requests = requests_311.dropna(subset=['lat'])

    # Step 2: Filter for specific service_name values
    service_names = [
        "Rubbish/Recyclable Material Collection",
        "Sanitation Violation",
        "Illegal Dumping",
        "Sanitation / Dumpster Violation",
        "Dumpster Violation"
    ]
    filtered_requests = filtered_requests[filtered_requests['service_name'].isin(service_names)]

    # Step 3: Convert to GeoDataFrame with specified CRS (EPSG:4326)
    trash = gpd.GeoDataFrame(
        filtered_requests,
        geometry=gpd.points_from_xy(filtered_requests['lon'], filtered_requests['lat']),
        crs='EPSG:4326'
    )

    # Step 4: Transform CRS to EPSG:6565
    trash = trash.to_crs(epsg=6565)

    sql1 = '''
        SELECT
            *,
            ST_GEOGPOINT(
            SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(1)] AS FLOAT64),
            SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(0)] AS FLOAT64)
            ) AS geography
            # ST_GeogFromGeoJson(geog) AS geography
        FROM
            `core.opa_properties` AS p
    '''
    
    sql2 = '''
        SELECT
            *,
            ST_GEOGPOINT(
            SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(1)] AS FLOAT64),
            SAFE_CAST(SPLIT(REPLACE(REPLACE(p.geog, 'POINT(', ''), ')', ''), ' ')[OFFSET(0)] AS FLOAT64)
            ) AS geography
        FROM
            `core.neighborhoods` AS p
    '''

    # Run the queries
    print('Extracting neighborhood data from BigQuery table')
    neighborhoods = bigquery_client.query_and_wait(sql2).to_dataframe()

    print('Extracting properties data from BigQuery table')
    properties = bigquery_client.query_and_wait(sql1).to_dataframe()
   
    print('Extracting landmarks and markets data from raw bucket')

    # Read GeoJSON data from GCS
    landmarks = read_geojson_from_gcs(bucket_name, "landmarks/landmarks.geojson").to_crs(epsg=6565)
    markets = read_geojson_from_gcs(bucket_name, "markets/markets.geojson").to_crs(epsg=6565)

    # Check for and remove "POINT EMPTY" geometries directly
    # def is_empty_point(geom):
    #     return geom.is_empty
    def drop_point_empty(gdf):
        return gdf[~gdf.geometry.is_empty]

    homicide = drop_point_empty(homicide)
    theft = drop_point_empty(theft)
    trash = drop_point_empty(trash)
    markets = drop_point_empty(markets)
    landmarks = drop_point_empty(landmarks)

    properties_copy = properties.copy()

    print('Cleaning data')

    # Filter and process data
    properties_copy = (
        properties.dropna(subset=['sale_price'])
        .merge(
            properties.groupby(['sale_date', 'sale_price']).size().reset_index(name='count'),
            on=['sale_date', 'sale_price']
        )
        .assign(is_bundle=lambda df: df['count'] > 1)
        .query('not is_bundle')
        .drop(columns=['count', 'is_bundle'])
        .query('sale_price > 10 & sale_price < 10000000 & total_livable_area > 0 & year_built > 0')
    )

    def convert_to_point(geog_str):
        # Extract coordinates from the string
        try:
            coord_str = geog_str.split('(')[1].split(')')[0]
            lon, lat = map(float, coord_str.split())
            return Point(lon, lat)
        except:
            return None

    # Apply the conversion
    properties_copy['geometry'] = properties_copy['geography'].apply(convert_to_point)

    # Drop rows where conversion failed
    properties_copy = properties_copy.dropna(subset=['geometry'])
    properties_copy = gpd.GeoDataFrame(properties_copy, geometry='geometry', crs="EPSG:4326")

    def map_exterior_condition(cond):
        if cond in ['0', '1', '2', '3', 0.0, 1.0, 2.0, 3.0]:
            return 'Above average'
        elif cond in ['4', '5', 4.0, 5.0]:
            return 'Average'
        elif cond in ['6', 6.0]:
            return 'Below average'
        elif cond in ['7', 7.0, 8.0, 'A']:
            return 'Others'
        elif lpd.isna(cond):  # Catch NaN first
            return 'Others'
        else:
            return np.nan

    properties_copy['exterior_condition_grp'] = properties_copy['exterior_condition'].apply(map_exterior_condition)

    properties_copy['exterior_condition_grp'] = lpd.Categorical(
        properties_copy['exterior_condition_grp'],
        categories=['Others', 'Below average', 'Average', 'Above average'],
        ordered=True
    )

    def map_interior_condition(cond):
        if cond in ['0', '1', '2', '3', 0.0, 1.0, 2.0, 3.0]:
            return 'Above average'
        elif cond in ['4', '5', 4.0, 5.0]:
            return 'Average'
        elif cond in ['6', 6.0]:
            return 'Below average'
        elif cond in ['7', 7.0, 8.0, 'A']:
            return 'Others'
        elif lpd.isna(cond):  # Catch NaN first
            return 'Others'
        else:
            return np.nan

    properties_copy['interior_condition_grp'] = properties_copy['interior_condition'].apply(map_interior_condition)

    properties_copy['interior_condition_grp'] = lpd.Categorical(
        properties_copy['interior_condition_grp'],
        categories=['Others', 'Below average', 'Average', 'Above average'],
        ordered=True
    )

    def map_central_air(air_code):
        if air_code in ['1', "Y"]:
            return "Y"
        elif air_code in ['0', "N"]:
            return "N"
        elif lpd.isna(air_code):
            return "Unknown"
        else:
            return np.nan

    properties_copy['central_air'] = (
        properties_copy['central_air']
        .apply(map_central_air)
    )

    properties_copy['central_air'] = lpd.Categorical(
        properties_copy['central_air'],
        categories=["Unknown", "N", "Y"],
        ordered=True
    )

    def map_fireplaces(fp):
        if fp == 0:
            return "0"
        elif fp >= 1:
            return "1+"
        elif lpd.isna(fp):
            return "Unknown"
        else:
            return np.nan

    properties_copy['fireplaces_grp'] = (
        properties_copy['fireplaces']
        .apply(map_fireplaces)
    )

    properties_copy['fireplaces_grp'] = lpd.Categorical(
        properties_copy['fireplaces_grp'],
        categories=["Unknown", "0", "1+"],
        ordered=True
    )

    def map_garage_spaces(spaces):
        if spaces == 0:
            return "0"
        elif spaces == 1:
            return "1"
        elif spaces > 1:
            return "2+"
        elif lpd.isna(spaces):
            return "Unknown"
        else:
            return np.nan

    properties_copy['garage_spaces_grp'] = (
        properties_copy['garage_spaces']
        .apply(map_garage_spaces)
    )

    properties_copy['garage_spaces_grp'] = lpd.Categorical(
        properties_copy['garage_spaces_grp'],
        categories=["Unknown", "0", "1", "2+"],
        ordered=True
    )

    def map_bedrooms(bedrooms):
        if lpd.isna(bedrooms):
            return "Unknown"
        elif bedrooms <= 5:
            return str(int(bedrooms))  # Convert to integer first to handle decimals
        elif bedrooms > 5:
            return "5+"
        else:
            return np.nan

    properties_copy['number_of_bedrooms_grp'] = (
        properties_copy['number_of_bedrooms']
        .apply(map_bedrooms)
    )

    properties_copy['number_of_bedrooms_grp'] = lpd.Categorical(
        properties_copy['number_of_bedrooms_grp'],
        categories=["Unknown", "0", "1", "2", "3", "4", "5", "5+"],
        ordered=True
    )

    def map_bathrooms(bathrooms):
        if lpd.isna(bathrooms):
            return "Unknown"
        elif bathrooms <= 2:
            return str(float(bathrooms))  # Keep as float to handle decimal bathrooms
        elif bathrooms > 2:
            return "2+"
        else:
            return np.nan

    properties_copy['number_of_bathrooms_grp'] = (
        properties_copy['number_of_bathrooms']
        .apply(map_bathrooms)
    )

    # Handle potential decimal formatting (e.g., 2.0 → "2.0")
    properties_copy['number_of_bathrooms_grp'] = (
        properties_copy['number_of_bathrooms_grp']
        .replace({'0.0': '0', '1.0': '1', '2.0': '2'})
    )

    properties_copy['number_of_bathrooms_grp'] = lpd.Categorical(
        properties_copy['number_of_bathrooms_grp'],
        categories=["Unknown", "0", "1", "2", "2+"],
        ordered=True
    )

    def map_stories(stories):
        if lpd.isna(stories):
            return "Unknown"
        elif stories <= 2:
            return str(int(stories))  # Convert to integer to handle decimals
        elif stories > 2:
            return "2+"
        else:
            return np.nan

    properties_copy['number_stories_grp'] = (
        properties_copy['number_stories']
        .apply(map_stories)
    )

    properties_copy['number_stories_grp'] = lpd.Categorical(
        properties_copy['number_stories_grp'],
        categories=["Unknown", "1", "2", "2+"],
        ordered=True
    )

    def map_heater_type(heater):
        if heater == "A":
            return "A"
        elif lpd.isna(heater):
            return "Unknown"
        else:
            return "Non-A"

    properties_copy['type_heater_grp'] = (
        properties_copy['type_heater']
        .apply(map_heater_type)
    )

    properties_copy['type_heater_grp'] = lpd.Categorical(
        properties_copy['type_heater_grp'],
        categories=["Unknown", "A", "Non-A"],
        ordered=True
    )

    # Calculate age
    properties_copy['age'] = datetime.now().year - properties_copy['year_built']

    # Create age groups
    def map_age_groups(age):
        if age <= 25:
            return "<= 25"
        elif 25 < age <= 75:
            return "26-75"
        elif 75 < age <= 100:
            return "76-100"
        elif 100 < age <= 125:
            return "101-125"
        else:
            return "126+"

    properties_copy['age_grp'] = (
        properties_copy['age']
        .apply(map_age_groups)
    )

    properties_copy['age_grp'] = lpd.Categorical(
        properties_copy['age_grp'],
        categories=["<= 25", "26-75", "76-100", "101-125", "126+"],
        ordered=True
    )

    def map_building_code(desc):
        if lpd.isna(desc) or desc == "":
            return "Unknown"
        elif str(desc).startswith("ROW"):
            return "Row"
        elif str(desc).startswith("TWIN"):
            return "Twin"
        else:
            return "Other"

    properties_copy['building_code_grp'] = (
        properties_copy['building_code_description_new']
        .apply(map_building_code)
    )

    properties_copy['building_code_grp'] = lpd.Categorical(
        properties_copy['building_code_grp'],
        categories=["Unknown", "Row", "Twin", "Other"],
        ordered=True
    )

    def map_quality_grade(grade):
        if lpd.isna(grade) or grade == "":
            return "Unknown"
        elif grade.strip() in ["A", "A-", "A+"]:
            return "A"
        elif grade.strip() in ["B", "B-", "B+"]:
            return "B"
        elif grade.strip() in ["C", "C-", "C+"]:
            return "C"
        elif grade.strip() in ["D", "D-", "D+"]:
            return "D"
        elif grade.strip() in ["E", "E-", "E+"]:
            return "E"
        elif grade.strip() in ["S", "S-", "S+"]:
            return "S"
        elif grade.strip() in ["X", "X-"]:
            return "X"
        else:
            return "Other"

    properties_copy['quality_grade_grp'] = (
        properties_copy['quality_grade']
        .apply(map_quality_grade)
    )

    properties_copy['quality_grade_grp'] = lpd.Categorical(
        properties_copy['quality_grade_grp'],
        categories=["Unknown", "A", "B", "C", "D", "E", "S", "X", "Other"],
        ordered=True
    )

    # Ensure the column is treated as strings
    properties_copy['sale_date'] = properties_copy['sale_date'].astype(str)

    # Complete manual parsing
    properties_copy['sale_year'] = properties_copy['sale_date'].str[:4]
    properties_copy['sale_month'] = properties_copy['sale_date'].str[5:7]

    # Convert to numeric
    properties_copy['sale_year'] = lpd.to_numeric(properties_copy['sale_year'], errors='coerce')
    properties_copy['sale_month'] = lpd.to_numeric(properties_copy['sale_month'], errors='coerce')

    properties_copy['sale_month'] = lpd.Categorical(
        properties_copy['sale_month'],
        categories=range(1, 13),
        ordered=True
    )

    properties_copy = properties_copy.to_crs(epsg=6565)

    print('Calculating nearest neighbors')

    def log_dist_feature(target_gdf, source_gdf, k_neighbors):
        """Calculate log(1 + mean distance) to k nearest neighbors"""
        # Convert CRS once
        target_crs = target_gdf.to_crs(epsg=6565)
        source_crs = source_gdf.to_crs(epsg=6565)

        # Create 2D coordinate arrays
        target = np.column_stack([target_crs.geometry.x, target_crs.geometry.y])
        source = np.column_stack([source_crs.geometry.x, source_crs.geometry.y])

        if len(source) == 0:
            return np.log1p(np.zeros(len(target_gdf)))

        tree = KDTree(source)
        dists, _ = tree.query(target, k=min(k_neighbors, len(source)))
        return np.log1p(dists.mean(axis=1))

    # Calculate features
    properties_copy['homicides'] = log_dist_feature(properties_copy, homicide, k_neighbors=3)
    properties_copy['trash_requests'] = log_dist_feature(properties_copy, trash, k_neighbors=5)
    properties_copy['markets'] = log_dist_feature(properties_copy, markets, k_neighbors=1)
    properties_copy['landmarks'] = log_dist_feature(properties_copy, landmarks, k_neighbors=50)
    properties_copy['thefts'] = log_dist_feature(properties_copy, theft, k_neighbors=7)

    def geojson_to_shape(geojson_str):
        """
        Converts a GeoJSON string to a shapely geometry object.
        """
        try:
            geojson = json.loads(geojson_str)
            return shape(geojson)
        except (TypeError, json.JSONDecodeError):
            return None

    # Apply the conversion
    neighborhoods['geometry'] = neighborhoods['geog'].apply(geojson_to_shape)

    # Drop rows where geometry creation failed
    neighborhoods = neighborhoods.dropna(subset=['geometry'])

    # Convert to GeoDataFrame
    neighborhoods = gpd.GeoDataFrame(neighborhoods, geometry='geometry', crs="EPSG:4326")

    # Reproject if needed
    neighborhoods = neighborhoods.to_crs(epsg=6565)

    # Spatial join with neighborhoods (keeping only MAPNAME column)
    properties_copy = gpd.sjoin(
        properties_copy,
        neighborhoods[["mapname", "geometry"]],  # Must include geometry column
        how="left",
        predicate="within"  # Use 'intersects' for boundary cases
    )

    # Rename column
    properties_copy = properties_copy.rename(columns={"mapname": "neighborhood"})

    # Remove properties with missing neighborhoods
    properties_copy = properties_copy[~properties_copy["neighborhood"].isna()]

    vars = ["objectid", "sale_price", "census_tract", "central_air", "location",
            "market_value", "total_livable_area", "exterior_condition_grp",
            "interior_condition_grp", "fireplaces_grp", "garage_spaces_grp",
            "number_of_bedrooms_grp", "number_of_bathrooms_grp", "number_stories_grp",
            "type_heater_grp", "age_grp", "building_code_grp", "quality_grade_grp",
            "sale_year", "sale_month", "homicides", "trash_requests", "markets",
            "landmarks", "thefts", "neighborhood"]

    properties_df = properties_copy[vars]

    print('Feature engineering and train test split')

    # 2. Feature Engineering
    X = properties_df[[
        'central_air', 'market_value', 'total_livable_area', 'exterior_condition_grp',
        'interior_condition_grp', 'fireplaces_grp', 'garage_spaces_grp',
        'number_of_bedrooms_grp', 'number_of_bathrooms_grp', 'number_stories_grp',
        'type_heater_grp', 'age_grp', 'building_code_grp', 'quality_grade_grp',
        'sale_year', 'sale_month', 'homicides', 'trash_requests', 'markets',
        'landmarks', 'thefts', 'neighborhood'
    ]]

    y = np.log(properties_df['sale_price'])

    year_counts = X['sale_year'].value_counts()
    valid_years = year_counts[year_counts >= 2].index
    X = X[X['sale_year'].isin(valid_years)]
    y = y[X.index]

    # 3. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=X['sale_year']
    )

    # 4. Preprocessing
    preprocessor = ColumnTransformer([
        # Numeric log transforms
        ('log_market_value', FunctionTransformer(np.log1p), ['market_value']),
        ('log_livable_area', FunctionTransformer(np.log1p), ['total_livable_area']),

        # Categorical features (month included)
        ('ohe', OneHotEncoder(handle_unknown='ignore'), [
            'central_air', 'exterior_condition_grp', 'interior_condition_grp',
            'fireplaces_grp', 'garage_spaces_grp', 'number_of_bedrooms_grp',
            'number_of_bathrooms_grp', 'number_stories_grp', 'type_heater_grp',
            'age_grp', 'building_code_grp', 'quality_grade_grp', 'neighborhood',
            'sale_month'  # Now explicitly treated as categorical
        ]),

        # Pass through remaining numerical features unchanged
    ], remainder='passthrough')

    print('Running model')

    # 5. Model Pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42,
                                            n_estimators=200,
                                            max_depth=20,
                                            max_features='sqrt',
                                            min_samples_leaf=1,
                                            min_samples_split=2))
    ])

    pipeline.fit(X_train, y_train)
    # 28 minutes 29 seconds

    print('Model ran!')

    # Get predictions (in log space)
    y_train_pred_log = pipeline.predict(X_train)

    # Smearing correction factor
    residuals_train = y_train - y_train_pred_log
    smearing_train_factor = np.sqrt(np.mean(residuals_train**2))

    # Convert to original scale with correction
    y_train_pred = np.exp(y_train_pred_log + 0.5 * smearing_train_factor**2)

    # Get predictions (in log space)
    y_pred_log = pipeline.predict(X_test)

    # Smearing correction factor
    residuals = y_test - y_pred_log
    smearing_factor = np.sqrt(np.mean(residuals**2))

    # Convert to original scale with correction
    y_pred = np.exp(y_pred_log + 0.5 * smearing_factor**2)

    # 4. Create Series from train/test
    train_predictions = lpd.Series(y_train_pred, index=X_train.index)
    test_predictions = lpd.Series(y_pred, index=X_test.index)

    # 5. Combine
    all_predictions = lpd.concat([train_predictions, test_predictions])

    # 6. Create output
    output = lpd.DataFrame({
        'property_id': properties_df.loc[all_predictions.index, 'objectid'],
        'tax_year': 2025,
        'sale_price_2025': all_predictions.values
    })

    filename = DATA_DIR / 'model_output.csv'
    output.to_csv(filename, index=False)

    print('Upload model output to temp bucket as csv')

    # Upload the csv file to cloud storage
    temp_bucket_name = 'musa5090s25-team5-temp_data'
    blobname = 'model_output/model_output.csv'
    temp_bucket = storage_client.bucket(temp_bucket_name)
    blob = temp_bucket.blob(blobname)
    blob.upload_from_filename(filename)
    print('Uploaded to temp bucket')

    return 'Model output in temp bucket!'
