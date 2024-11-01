import sys,os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTE_PARAMS
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformation_object(cls)->Pipeline:
        """KNN IMPUTER

        Returns:
            Pipeline: with data transformation params
        """
        
        
        logging.info("Entered get_data_transformation_object of DataTranformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTE_PARAMS}"
            )
            processor:Pipeline = Pipeline([("Imputer",imputer)])
            
            
            return processor        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
            
    
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        logging.info("Entering data_transformation method of DataTransformation class")
        try:
            logging.info("starting data_transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## dropping target variable 
            
            X_train = train_df.drop([TARGET_COLUMN],axis=1)
            
            y_train = train_df[TARGET_COLUMN]
            y_train = y_train.replace(-1,0)
            
            X_test = test_df.drop([TARGET_COLUMN],axis= 1)
            y_test = test_df[TARGET_COLUMN]
            y_test = y_test.replace(-1,0)
            
            preprocessor = self.get_data_transformation_object()
            preprocessor_obj= preprocessor.fit(X_train)
            X_train_trans= preprocessor.transform(X_train)
            X_test_trans = preprocessor.transform(X_test)
            
            train_arr = np.c_[X_train_trans, np.array(y_train)]
            test_arr = np.c_[X_test_trans, np.array(y_test)]
            
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)
            
            # artifacts
            
            data_transformation_artifact = DataTransformationArtifact(transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                                                                      transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                                                                      transformed_test_file_path = self.data_transformation_config.transformed_test_file_path)
                                    

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
        
        
        

 



