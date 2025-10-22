## Contains the code of reading the dataset....

## Importing libraries:

import os
import sys # because our to use our custom exception:
import pandas as pd
from src.exception import CustomException
from src.logger import logging


from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:   ## to save the files path config files
    train_data_path : str=os.path.join('artifacts','train.csv')
    test_data_path : str=os.path.join('artifacts','test.csv')
    raw_data_path : str=os.path.join('artifacts','data.csv')

## we dont need to use the decorator when we have to define a function in class...

class DataIngestion:
    def __init__(self):
        self.ingestionconfig=DataIngestionConfig() ## This calls the DataIngestionConfig function and this variable store all the path info:


    def initiate_data_ingestion(self): ## TO read the data and save:
        logging.info("--- Data Reading is Started ---")
        try:

            df=pd.read_csv('notebook/data/stud.csv')
            #create the directories for file saving:

            os.makedirs(os.path.dirname(self.ingestionconfig.test_data_path),exist_ok=True)
            df.to_csv(self.ingestionconfig.raw_data_path,index=False,header=True)
        
            logging.info('Created the Directory path and Raw Data File')

            logging.info("Train Test Split is Started:")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestionconfig.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestionconfig.test_data_path,index=False,header=True)

            logging.info("--- Ingestion of the Data is completed ---")

            return(
                self.ingestionconfig.train_data_path,
                self.ingestionconfig.test_data_path
            )


        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=='__main__':
    obj=DataIngestion()
    obj.initiate_data_ingestion()
        




