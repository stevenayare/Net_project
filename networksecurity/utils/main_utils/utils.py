import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

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