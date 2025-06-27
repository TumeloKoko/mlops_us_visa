import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from us_visa.exception import USvisaException
from us_visa.logger.logging_utils import LoggerManager


class TargetValueMapping:
    def __init__(self):
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        self.Certified: int = 0
        self.Denied: int = 1
        
    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
    
class USvisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """ 
        :param preprocessing_object : Input object of preprocessor
        :param trained_model_object : Input object of trained model
        """
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        
        
    def predict(self, dataframe: DataFrame) -> DataFrame:
        """ 
        Function accepts raw inputs and then transforms raw input(prompt) using the preprocessing_object which
        guarantees that the inputs are in the same format as the training data
        At last it performs the prediction on transformed features
        """
        
        self.logging.info("Entered the predict method of USvisaModel class")
        
        try:
            self.logging.info("Using the the preprocessor to transform data")
            transformed_features = self.preprocessing_object.transform(dataframe)
            
            self.logging.info("Used the trained model to get predictions")
            self.logging.info("Exited the predict method of USvisaModel class")            
            return self.trained_model_object.predict(transformed_features)
        
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"
        
    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"