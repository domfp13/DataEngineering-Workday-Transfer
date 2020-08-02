# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

#External Libs
from typing import Optional
from functools import partial
from os import getcwd
from pathlib import Path
import logging

# Local imports
from etl.GenericFunctions import copyFileToAnotherLocalDestination
from etl.S3Classes import S3Client

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
loggin_file_path = str(Path('{path}/LOGGER.log'.format(path = getcwd())))
logging.basicConfig(filename = loggin_file_path,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')

logger = logging.getLogger()

if __name__ == '__main__':
    try:
        logger.info("01. Creating instance of S3Client")
        s3 = S3Client(bucket_name='domfp13-s3-bucket', prefix='hr_files')

        logger.info("02. Getting the list of files to download")
        s3.listOfFilesToDownload()
        
        logger.info("03. Checking if list is empty")
        if s3.files_to_download:
            
            logger.info("04. Downloading files locally in directory out")
            s3.downloadFilesFromS3()

            logger.info("05. Moving files to another directory")
            list(map(copyFileToAnotherLocalDestination, s3.files_to_move))
            
    except Exception as e:
        logger.exception(e)
