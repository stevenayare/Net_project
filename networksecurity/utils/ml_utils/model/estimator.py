import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME,TARGET_COLUMN
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

class classificationModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
            
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_featured_label(self,x):
        y = x[TARGET_COLUMN]
        y.replace(-1,0,inplace=True)
        
        return y
        
    
    def predict(self,x):
        try:
            if "Result" in x.columns: 
                x= x.drop(["Result"],axis= 1)
                
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            
            return y_pred
        
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)    