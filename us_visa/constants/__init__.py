import os
from pathlib import Path
from from_root import from_root
from datetime import date
from dotenv import load_dotenv

DATABASE_NAME = "US_VISA"

COLLECTION = "visa_data"

env_path = Path("../../")/".env.local"
load_dotenv(dotenv_path=env_path)

MONGODB_URL_KEY = os.environ.get("MONGODB_URL") 

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"

FILE_NAME = "usvisa.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preproccessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

AWS_ACCESS_KEY_ID_ENV_KEY = os.environ.get("AWS_ACCESS_KEY_ID") 
AWS_SECRET_ACCESS_KEY_ENV_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY") 
REGION_NAME = "eu-north-1"

""" 
Data Ingestion related constants:
    Start with 'DATA_INGESTION' variable name
"""
DATA_INGESTION_COLLECTION_NAME: str = COLLECTION
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


""" 
Data Validation related constants:
    Start with 'DATA_VALIDATION' variable name
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"


""" 
Data Transformation related constants:
    Start with 'DATA_TRANSFORMATION' variable name
"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


""" 
Model Trainer related constants:
    Start with 'MODEL_TRAINER' variable name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH = os.path.join("config", "model.yaml")


""" 
Model Evaluation related constants:
    Start with 'MODEL_EVALUATION' variable name
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.2
MODEL_BUCKET_NAME = "mlops-projects-usvisa-model-2025"
MODEL_PUSHER_S3_KEY = "model-registry"


""" 
App related constants
"""
APP_HOST = "0.0.0.0"
APP_PORT = 8080