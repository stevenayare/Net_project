import os, sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.utils.main_utils.utils import save_object,load_object,load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import classificationModel
from networksecurity.entity.config_entity import ModelTrainerConfig
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier, 
    
)
import mlflow




class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact): 
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model, classificationmetric):
        
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score
            
            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model") 
         
        
    
    def train_model(self,X_train,y_train,X_test,y_test): ## training and testing together to avoid extra modules
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "AdaBoost": AdaBoostClassifier()
            
        }
        
        params={
            
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                 
                'n_estimators': [8,16,32,128,256]
            },
            "Logistic Regression":{},
            "Gradient Boosting":{
                 
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
               
                'n_estimators': [8,16,32,64,128,256]
            },
            
            
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        
        model_report:dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                            models = models, params = params)
        
        best_model_score = max(sorted(model_report.values()))
        
        
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_train,y_train_pred)
        
        ## tracking
        self.track_mlflow(best_model, classification_train_metric)
        
        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_test,y_test_pred)
        self.track_mlflow(best_model, classification_test_metric)
        
        preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)
        
        
        Classification_Model = classificationModel(preprocessor = preprocessor,model = best_model)
        save_object(file_path = self.model_trainer_config.trained_model_file_path,obj = Classification_Model)
        
        
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                                                    train_metric_artifact = classification_train_metric, test_metric_artifact = classification_test_metric
                                                    )
        
        logging.info(f"Model Trainer Artifact is : {model_trainer_artifact}")
        
        return model_trainer_artifact
        
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            X_train,y_train, X_test, y_test = ( 
                  
                  train_arr[:,:-1], 
                  train_arr[:,-1], 
                  test_arr[:,:-1],
                  test_arr[:,-1],
            )
            
            model_trainer_artifact = self.train_model(X_train, y_train,X_test,y_test) 
            
            return model_trainer_artifact 
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)        