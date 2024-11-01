import os
import sys
import streamlit as st
import pymongo
import certifi
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv('MONGODB_URL_KEY')

# MongoDB connection setup
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Streamlit page setup
st.title('Network Security Training Interface')

# Button to trigger the training pipeline
if st.button('Start Training Pipeline'):
    try:
        logging.info("Starting training pipeline.")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()

        logging.info("Training pipeline completed successfully.")
        st.success("Training completed successfully.")
    except Exception as e:
        logging.error("Error in training pipeline", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
        raise NetworkSecurityException(e, sys)

# Display MongoDB connection status
if client:
    st.info(f"Connected to MongoDB at {mongo_db_url}")
else:
    st.error("Failed to connect to MongoDB.")
