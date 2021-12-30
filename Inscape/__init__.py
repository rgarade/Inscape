import configparser
import logging
import logging.handlers as handlers
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler




initfile="config/config.ini"
configParser = configparser.ConfigParser()
configParser.read(initfile)



path = configParser.get('LOG_DETAILS', 'foldername')
if not os.path.exists(path):
    os.makedirs(path)




#logger
log_file = configParser.get('LOG_DETAILS', 'filename')
# print("..........file:",log_file)
# log_file1 = os.path.abspath(path)
# print(".................................................",log_file1)
file_size = configParser.get('LOG_DETAILS', 'maxbytes')
file_size=int(file_size)
file_count = configParser.get('LOG_DETAILS', 'backupCount')
file_count=int(file_count)

logger = logging.getLogger()
if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s -%(lineno)d - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    logHandler = ConcurrentRotatingFileHandler(log_file, maxBytes=file_size, backupCount=file_count)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
logger.info("logger implemented")
