import io
import os
import sys
import boto3

from botocore.exceptions import ReadTimeoutError

class LocalCachedS3Storage:
    MAX_RETRY = 3
    RETRY_WAIT = 3 # secs

    CACHE_DIR = ".cache"

    def __init__(self, bucket, cache_enabled):
        self.s3 = boto3.resource('s3')
        self.bucket = bucket
        self.cache_enabled = cache_enabled

    def put(self, key, data):
        obj = self.s3.Object(self.bucket, key)
        obj.put(Body=data)
        if self.cache_enabled: self.__write_local(key, data)

    def get(self, key):
        if self.cache_enabled:
            local_filename = self.__cache_filename(key)
            if os.path.isfile(local_filename):
                with open(local_filename,'r') as f:
                    return f.read()

        retry_count = 0
        while(retry_count < self.MAX_RETRY):
            try:
                obj = self.s3.Object(self.bucket, key)
                data = obj.get()['Body'].read().decode('utf-8')
                if self.cache_enabled: self.__write_local(key, data)
                return data
            except ReadTimeoutError:
                retry_count+=1
                sleep(self.RETRY_WAIT * retry_count)

    def __write_local(self, key, data):
        local_filename = self.__cache_filename(key)
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)
        with open(local_filename, "w+") as file:
            file.write(data)

    def __cache_filename(self, key):
        return f"{self.CACHE_DIR}/{self.bucket}/{key}"
