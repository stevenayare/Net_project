import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle
from sklearn.metrics import f1_score

from sklearn.model_selection import RandomizedSearchCV

def read_yaml_file(file_path: str) ->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e   

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)            
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content,yaml_file)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)        


def save_numpy_array_data(file_path:str, array: np.array):    
    try:
        logging.info('Entered save_numpy_array_data method')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as obj_path:
            np.save(obj_path,array)
        logging.info('Exited save_numpy_array_data method and saved array ')
    except Exception as e:
        raise NetworkSecurityException(e,sys)    
def save_object(file_path:str, obj: object):    
    try:
        logging.info('Entered save object  method')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as obj_path:
            pickle.dump(obj,obj_path)
        logging.info('Exited save object method and saved object ')
    except Exception as e:
        raise NetworkSecurityException(e,sys)        
def load_object(file_path: str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File path {file_path}%s does not exist")
        with open(file_path, 'rb') as obj_path:
            print(obj_path)
            
            return pickle.load(obj_path)
            
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)    

def load_numpy_array_data(file_path: str)->np.array:
        try:
            with open(file_path, 'rb') as file_obj:
                return np.load(file_obj)
         
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
def evaluate_models(X_train, y_train,X_test, y_test, models:dict, params: dict)->dict:
    try:
        report= {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = list(params.values())[i]
            
            rs = RandomizedSearchCV(model,param,cv =3)
            rs.fit(X_train,y_train)
            
            model.set_params(**rs.best_params_)
            model.fit(X_train,y_train)
            y_train_pred = rs.predict(X_train)
            y_test_pred = rs.predict(X_test)
            
            
            train_model_score = f1_score(y_train,y_train_pred)
            test_model_score = f1_score(y_test,y_test_pred)
            
            
            report[list(models.keys())[i]] = test_model_score # hashing
        
        
        
        return report              
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)        