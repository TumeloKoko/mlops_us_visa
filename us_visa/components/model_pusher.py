import sys

from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.entity.config_entity import ModelPusherConfig
from us_visa.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from us_visa.entity.s3_estimator import USvisaEstimator

from us_visa.exception import USvisaException
from us_visa.logger.logging_utils import LoggerManager

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact, model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.logging = LoggerManager(self.__class__.__name__).get_logger()
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.usvisa_estimator = USvisaEstimator(bucket_name=model_pusher_config.bucket_name,
                                                model_path=model_pusher_config.s3_model_key_path
                                                )
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model pusher
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        
        self.logging.info("Entered the initiate_model_evaluation method of ModelPusher class")
        
        try:
            self.logging.info("Uploading artifacts folder to s3 bucket")
            self.usvisa_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name, s3_model_path=self.model_pusher_config.s3_model_key_path)
            
            self.logging.info("Uploaded artifacts folder to s3 bucket")
            self.logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            self.logging.info("Exited the initiate_model_evaluation method of ModelPusher class")
            
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e