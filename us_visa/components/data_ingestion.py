import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

from us_visa.entity.config_entity import DataIngestionConfig # Pipeline Input
from us_visa.entity.artifact_entity import DataIngestionArtifact # Pipeline Output
from us_visa.data_access.usvisa_data import UsVisaData

from us_visa.exception import USvisaException
from us_visa.logger.logging_utils import LoggerManager



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """ 
        param: data_ingestion_config -> configuration for data ingestion
        """
        
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """ 
        Method Name : export_data_into_feature_store
        Description : This method exports data from mongodb into csv file
        
        Output      : data is returned as artifact of data ingestion components
        On Failure  : Write an exception log and then raise an exception
        """
        
        try:
            self.logging.info(f"Exporting data from MongoDB")
            usvisa_data = UsVisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name= self.data_ingestion_config.collection_name)  
            self.logging.info(f"Shape of dataframe: {dataframe.shape}")
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            self.logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            
            dataframe.to_csv(feature_store_file_path, index= False, header= True)
            
            return dataframe

        except Exception as e:
            raise USvisaException(e, sys) from e
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """ 
        Method Name   : split_data_as_train_test
        Description   : This method splits the dataframe into train set and test set based on split ratio

        Output        : Folder is created in s3 bucket
        On Failure    : Write and exception log and then raise an exception
        """
        
        self.logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            self.logging.info("Performed train test split on the dataframe")
            self.logging.info("Exited the split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            self.logging.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index= False, header= True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index= False, header= True)
            
            self.logging.info(f"Exported train and test file path")
            
        except Exception as e:
            raise USvisaException(e, sys) from e
    
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """ 
        Method Name     : initiate_data_ingestion
        Description     : This method initiates the data ingestion components of training pipeline
        
        Output          : train set and test set are returned as the artifacts of the data ingestion components
        On Failure      : Write and exception log and then raise an exception
        """
        
        self.logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        
        try:
            dataframe = self.export_data_into_feature_store()
            self.logging.info("Got the data from mongodb")
            
            self.split_data_as_train_test(dataframe)
            self.logging.info("Performed train test split on the dataset")
            
            self.logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path= self.data_ingestion_config.training_file_path,
                                                            test_file_path= self.data_ingestion_config.testing_file_path)
            
            self.logging.info(f"Data ingestion artifact : {data_ingestion_artifact}")
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise USvisaException(e, sys) from e
