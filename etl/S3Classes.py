# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from typing import Optional

class S3Client:
    def __init__(self, bucket_name:str='domfp13-s3-bucket', prefix:str='hr_files'):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.client = self.getS3Client()
    
    def decoratorGetS3Client(function):
        def wrapper():
            import boto3
            return boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
        return wrapper
    #@decoratorGetS3Client
    def getS3Client(self):
        import boto3
        return boto3.client('s3')
    
    def listOfFilesToDownload(self):
        """Returns a list containing the objects "Keys" to download, this is based on todays date.
        """
        # Adding some extra libs
        from datetime import datetime
        from pytz import timezone
        
        try:
            files_to_download = [] # This list will hold the objcts key
            
            time = datetime.now(timezone('US/Eastern')).strftime('%Y%m%d')
            prefix_with_date = "{prefix}/{year}/{month}/{day}/".format(prefix=self.prefix, year=time[0:4], month=time[4:6], day=time[6:])
            response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix_with_date)

            # If 0 then prefix does not exists, 1 prefix is empty, 2+ there is one or more files.
            if response['KeyCount'] >= 2:
                for obj in response['Contents']:
                    if obj['Key'] != prefix_with_date:
                        files_to_download.append(obj['Key'])

        except Exception as e:
            pass
        finally:
            self.files_to_download = files_to_download
    
    def downloadFilesFromS3(self)->None:
        """Download S3 object locally [out] directory.
        """
        from etl.GenericFunctions import getPath
        from os.path import basename

        files_to_move = []

        for element in self.files_to_download:
            path = getPath(basename(element))
            with open(path, 'wb') as f:
                self.client.download_fileobj(self.bucket_name, element, f)
            files_to_move.append(path)
        
        self.files_to_move = files_to_move