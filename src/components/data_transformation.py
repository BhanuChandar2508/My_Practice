## Contains the code of EDA steps and Transformation of data steps...:

## Importing libraries:

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import sys
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
#from src.components.data_ingestion import DataIngestionConfig
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformerConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformerConfig()
        #self.data_ingestion_config=DataIngestionConfig()


    def data_transformer_object(self):
        try:

            logging.info("--- Data Transformation is started ---")
            #raw_data_path = self.data_ingestion_config.raw_data_path
            #df=pd.read_csv(raw_data_path)
            #logging.info('categorizing the data into num and cateforical')
            numerical_columns=['writing_score','reading_score']
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course']

            logging.info(f"Numerical Columns:{numerical_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")


            logging.info("Creating The Pipeline for Numerical and Categorical columns:")

            num_pipeline=Pipeline(
                steps=[
                    ('num_imputer',SimpleImputer(strategy='median')),
                    ('scalar',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('cat_imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoding',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            logging.info("Pipelines were Created")

            preprocessor = ColumnTransformer(
                [
                    ('numerical_pipeline',num_pipeline,numerical_columns),
                ('categorical_pipeline',cat_pipeline,categorical_columns)
                ]

            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
        try:
            
            logging.info("Initiate Data Transformation is started")

            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            target_column='math_score'
            numerical_columns=['reading_score','writing_score']

            input_training_df=train_df.drop(columns=[target_column],axis=1)
            target_training_df=train_df[target_column]

            input_test_df=test_df.drop(columns=[target_column],axis=1)
            target_test_df=test_df[target_column]
            
            logging.info("Train Dataset and Test Dataset Were Set")
            logging.info("Setting Up preprocessor for Transformation")

            preprocessor_obj=self.data_transformer_object()
            input_training_arr=preprocessor_obj.fit_transform(input_training_df)
            input_test_arr=preprocessor_obj.transform(input_test_df)

            logging.info("Preprocessor is initialized successfully")
            train_arr=np.c_[input_training_arr,np.array(target_training_df)]
            test_arr=np.c_[input_test_arr,np.array(target_test_df)]

            
            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj)
            logging.info(f"Saving the Preprocessor/Model into pkl file at: {self.data_transformation_config.preprocessor_obj_file_path}")
            logging.info("--- Data Transformation is completed ---")
            return (train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
            
        except Exception as e:
            raise CustomException(e,sys)
