import os
import sys

from dataclasses import dataclass

import pandas as pd
import numpy as np
import scipy.sparse as sp

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object_sparse
import joblib

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.npz")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, transformed_df):
        try:
            logging.info("Splitting training and testing input data")

            cv = CountVectorizer(max_features=5000, stop_words='english')
            vectors = cv.fit_transform(transformed_df['tags'])

            cv.get_feature_names_out()

            similarity = cosine_similarity(vectors, dense_output=False)
            

            save_object_sparse(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=similarity
            )
            
            logging.info("Model trained successfully")

            return similarity, self.model_trainer_config.trained_model_file_path
        
        except Exception as e:
            raise CustomException(e, sys)