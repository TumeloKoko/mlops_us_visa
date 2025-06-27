import sys

from us_visa.exception import USvisaException
from us_visa.logger.logging_utils import LoggerManager

from us_visa.entity.config_entity import (
                                            DataIngestionConfig,
                                            DataValidationConfig,
                                            DataTransformationConfig,
                                            ModelTrainerConfig,
                                            ModelEvaluationConfig,
                                            ModelPusherConfig
                                        ) # Pipeline Input
from us_visa.entity.artifact_entity import (
                                            DataIngestionArtifact,
                                            DataValidationArtifact,
                                            DataTransformationArtifact,
                                            ModelTrainerArtifact,
                                            ModelEvaluationArtifact,
                                            ModelPusherArtifact
                                        ) # Pipeline Output

from us_visa.components.data_ingestion import DataIngestion # Method/Process
from us_visa.components.data_validation import DataValidation # Method/Process
from us_visa.components.data_transformation import DataTransformation # Method/Process
from us_visa.components.model_trainer import ModelTrainer # Method/Process
from us_visa.components.model_evaluation import ModelEvaluation # Method/Process
from us_visa.components.model_pusher import ModelPusher # Method/Process

class TrainPipeline:
    
    def __init__(self):
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
        
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the data ingestion component
        """
        
        self.logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            
            self.logging.info("Getting the data from MongoDB")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            self.logging.info("Got the train_set and test_set from MongoDB")
            
            self.logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the data validation component
        """
        
        self.logging.info("Entered the start_data_validation method of TrainPipeline class")
        try:
            data_validation = DataValidation(
                data_ingestion_artifact= data_ingestion_artifact,
                data_validation_config= self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            
            self.logging.info("Performed the data validation operation")
            
            self.logging.info("Exited the start_data_validation method of TrainPipeline class")
            
            return data_validation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the data transformation component
        """
        
        self.logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifact= data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config= self.data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            self.logging.info("Performed the data transformation operation")
            
            self.logging.info("Exited the start_data_transformation method of TrainPipeline class")
            
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the model training component
        """
        
        self.logging.info("Entered the start_model_trainer method of TrainPipeline class")
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact= data_transformation_artifact,
                model_trainer_config= self.model_trainer_config)
            
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            
            self.logging.info("Performed the model training operation")
            
            self.logging.info("Exited the start_model_trainer method of TrainPipeline class")
            
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the model evaluation component
        """
        
        self.logging.info("Entered the start_model_evaluation method of TrainPipeline class")
        try:
            model_evaluation = ModelEvaluation(
                data_ingestion_artifact= data_ingestion_artifact,
                model_trainer_artifact= model_trainer_artifact,
                model_eval_config= self.model_evaluation_config)
            
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            
            self.logging.info("Performed the model evaluation operation")
            
            self.logging.info("Exited the start_model_evaluation method of TrainPipeline class")
            
            return model_evaluation_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        
    def start_model_pusher(self,  model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """ 
        This method of TrainingPipeline is responsible for starting the model pusher component
        """
        
        self.logging.info("Entered the start_model_pusher method of TrainPipeline class")
        try:
            model_pusher = ModelPusher(
                model_evaluation_artifact= model_evaluation_artifact,
                model_pusher_config= self.model_pusher_config)
            
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            
            self.logging.info("Performed the model pusher operation")
            
            self.logging.info("Exited the start_model_pusher method of TrainPipeline class")
            
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        
        

    def run_pipeline(self, ) -> None:
        """ 
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact, model_trainer_artifact=model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                self.logging.info("Model not accepted")
                return None
            else:
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
                
        except Exception as e:
            raise USvisaException(e, sys) from e