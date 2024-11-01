import sys
import os
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
import streamlit as st
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import classificationModel as NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

# MongoDB connection setup
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

# Access the specific collection in the database
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Set up the Streamlit interface
st.title("Network Security Model Interface")

# Database connection status
if client:
    st.sidebar.success("Connected to MongoDB")
else:
    st.sidebar.error("Failed to connect to MongoDB")

# Training button
if st.button("Run Training Pipeline"):
    try:
        logging.info("Starting training pipeline.")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        st.success("Training completed successfully.")
    except Exception as e:
        logging.error(f"Training failed: {str(e)}", exc_info=True)
        st.error("Training failed.")
        raise NetworkSecurityException(e, sys)

# Prediction upload and processing
uploaded_file = st.file_uploader("Upload your file for prediction", type=["csv"])
if uploaded_file is not None:
    try:
        # Read data
        df = pd.read_csv(uploaded_file)
        preprocessor = load_object("final_models/preprocessor.pkl")
        model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        
        y_pred = network_model.predict(df)
        df['predicted_outcome'] = y_pred

        # Display results
        y_true = network_model.get_featured_label(df)
        metric_results = get_classification_score(y_true,y_pred) 
        f1_score = float(metric_results.f1_score) * 100         
        st.write(f"Prediction Output: f1_score: {round(f1_score,2)}")
        
        
        st.dataframe(df)
        df.to_csv('prediction_output/output.csv', index=False)
        st.success("Predictions added to DataFrame and saved.")
    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}", exc_info=True)
        st.error("Prediction failed.")
        raise NetworkSecurityException(e, sys)

# Optional: To run the Streamlit app from the script
# if __name__ == "__main__":
#     st.run()
