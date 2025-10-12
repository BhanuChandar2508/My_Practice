## Contains the logging information


import logging
import os
from datetime import datetime

LOG_File = f"{datetime.now().strftime('%m_%d_%Y_%H_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)

Log_File_path = os.path.join(log_path,LOG_File)


logging.basicConfig(
    filename=Log_File_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

#if __name__ == '__main__':
#    logging.info("Logging has Started...")
