import sys

import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact, DataIngestionArtifact

from us_visa.exception import USvisaException
from us_visa.logger.logging_utils import LoggerManager

from us_visa.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from us_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                data_validation_artifact: DataValidationArtifact):
        """ 
        :param data_ingestion_artifact      : Output reference of data ingestion artifact stage
        :param data_transformation_config   : configuration for data transformation
        :param data_validation_artifact     : Output reference of data validation artifact stage
        """
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(filepath=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def get_data_transformer_object(self) -> Pipeline:
        """ 
        Method Name         : get_data_transformer_object
        Description         : This method creates and returns a data transformer object for the data
        
        Output              : data transformer object is created and returned
        On Failure          : Write an exception log and raise an exception
        """
        
        self.logging.info("Entered get_data_transformer_object method of DataTransformation class")
        
        try:
            self.logging.info("got columns from schema file")
            num_features = self._schema_config["num_features"]
            ordinal_columns = self._schema_config["ordinal_columns"]
            onehot_columns = self._schema_config["onehot_columns"]
            transform_columns = self._schema_config["transform_columns"]
            
            self.logging.info("Initialized StandardScale, OneHotEncoder and OrdinalEncoder")
            numeric_transformer = StandardScaler()
            onehot_transformer = OneHotEncoder()
            ordinal_transformer = OrdinalEncoder()
            
            self.logging.info("Initialize PowerTransformer")
            transform_pipe = Pipeline(steps=[
                ("transformer", PowerTransformer(method="yeo-johnson"))
            ])
            
            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", onehot_transformer, onehot_columns),
                    ("OrdinalEncoder", ordinal_transformer, ordinal_columns),
                    ("Transformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features)
                ]
            )
            
            self.logging.info("Created preprocessor object from ColumnTransformer")
            
            self.logging.info("Exited get_data_transformer_object method of DataTransformation class")
            
            return preprocessor
            
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """ 
        Method Name         : initiate_data_transformation
        Description         : This method initiates the data transformation component for the pipeline
        
        Output              : data transformer steps are performed and preprocessor object is created
        On Failure          : Write an exception log and raise an exception
        """
        
        self.logging.info("Entered initiate_data_transformation method of DataTransformation class")
        
        try:
            if self.data_validation_artifact.validation_status:
                self.logging.info("Starting the data transformation")
                
                preprocessor = self.get_data_transformer_object()
                self.logging.info("Got the preprocessor object")
                
                train_df = DataTransformation.read_data(file_path= self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path= self.data_ingestion_artifact.test_file_path)
                
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                
                self.logging.info("Got train features and test features of Training dataset")
                
                input_feature_train_df["company_age"] = CURRENT_YEAR - input_feature_train_df["yr_of_estab"]
                
                self.logging.info("Added company age column to the Training dataset")
                
                drop_cols = self._schema_config["drop_columns"]
                
                self.logging.info("Drop the columns in drop_cols of Training dataset")
                
                input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)
                
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )
                
                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                
                self.logging.info("Got test features and test features of Testing dataset")
                
                input_feature_test_df["company_age"] = CURRENT_YEAR - input_feature_test_df["yr_of_estab"]
                
                self.logging.info("Added company age column to the Testing dataset")
                
                self.logging.info("Drop the columns in drop_cols of Testing dataset")
                
                input_feature_test_df = drop_columns(df=input_feature_test_df, cols=drop_cols)
                
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                
                self.logging.info("Got train and test features of Testing dataset")
                
                self.logging.info("Applying preprocessing object on training and testing dataframe")
                
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                
                self.logging.info("Used the preprocessor object to fit transform the train features")
                
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)
                
                self.logging.info("Used the preprocessor object to fit transform the test features")
                
                self.logging.info("Applying SMOTEEN on training dataset")
                
                smt = SMOTEENN(sampling_strategy="minority")
                
                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )
                self.logging.info("Applied SMOTEEN on training dataset")
                
                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )
                self.logging.info("Applied SMOTEEN on testing dataset")
                
                self.logging.info("Created train and test array")
                
                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]
                
                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]
                
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
                self.logging.info("Saved the preprocessor object")
                
                self.logging.info("Exited initiate_data_transformation method of DataTransformation class")
                
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                )
                
                return data_transformation_artifact
                
        except Exception as e:
            raise USvisaException(e, sys) from e