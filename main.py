from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation   
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion...")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info(" Data ingestion completed successfully")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info(" Data validation initialized successfully")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(" Data validation completed successfully")
        print(data_validation_artifact)
        data_transfomration_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info(" Data Transformation initialized successfully")
        data_transformation = DataTransformation(data_validation_artifact, data_transfomration_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(" Data Transformation completed successfully")
        print(data_transformation_artifact)
            
        
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)