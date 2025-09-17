import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            credits = pd.read_csv('notebook/data/tmdb_5000_credits.csv')
            movies = pd.read_csv('notebook/data/tmdb_5000_movies.csv')

            logging.info('Read the dataset as dataframe')
            df = movies.merge(credits, on='title')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            
            logging.info("Ingestion of the data is completed")

            return self.ingestion_config.raw_data_path

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    raw_data_path = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    transformed_df , _ = data_transformation.initiate_data_transformation(raw_data_path)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(transformed_df))