import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

class classificationModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
            
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            
            return y_pred
        
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    