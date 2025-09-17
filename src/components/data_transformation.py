import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
import ast
import nltk

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from nltk.stem.porter import PorterStemmer

import os
import pickle

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    ps = PorterStemmer()

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            pass

        except Exception as e:
            logging.error("Error occurred while creating data transformer object")
            raise CustomException(e, sys)

    def convert(self, obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L

    def convert3(self, obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter != 3:
                L.append(i['name'])
                counter += 1
            else:
                break
        return L

    def fetch_director(self, obj):
        L = []
        
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
        return L

    def stem(self, text):
        y = []
        ps = PorterStemmer()
        for i in text.split():
            y.append(ps.stem(i))
        return " ".join(y)
            
    def initiate_data_transformation(self, raw_data_path):
        try:
            df = pd.read_csv(raw_data_path)
            logging.info("Read raw data completed")

            df = df[['movie_id','title','overview','genres','keywords','cast','crew']]
            df.dropna(inplace=True)

            df['genres'] = df['genres'].apply(self.convert)

            df['keywords'] = df['keywords'].apply(self.convert)

            df['cast'] = df['cast'].apply(self.convert3)

            df['crew'] = df['crew'].apply(self.fetch_director)

            df['overview'] = df['overview'].apply(lambda x:x.split())

            df['genres'] = df['genres'].apply(lambda x:[i.replace(" ","") for i in x])

            df['keywords'] = df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

            df['cast'] = df['cast'].apply(lambda x:[i.replace(" ","") for i in x])

            df['crew'] = df['crew'].apply(lambda x:[i.replace(" ","") for i in x])

            df['tags'] = df['overview'] + df['genres'] + df['cast'] + df['crew']

            new_df = df[['movie_id','title','tags']]

            new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

            new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

            new_df['tags'] = new_df['tags'].apply(self.stem)
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=new_df
            )
            logging.info("Saved preprocessing object")

            return (new_df,self.data_transformation_config.preprocessor_obj_file_path)

        except Exception as e:
            logging.error("Error occurred during data transformation")
            raise CustomException(e, sys)