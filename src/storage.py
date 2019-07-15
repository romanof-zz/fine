import io
import os
import sys
import boto3

from botocore.exceptions import ReadTimeoutError

class S3Storage:
    MAX_RETRY = 3
    RETRY_WAIT = 3

    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.bucket = bucket

    def put(self, key, data):
        obj = self.s3.Object(self.bucket, key)
        obj.put(Body=data)

    def get(self, key):
        retry_count = 0
        while(retry_count < self.MAX_RETRY):
            try:
                obj = self.s3.Object(self.bucket, key)
                return obj.get()['Body'].read().decode('utf-8')
            except ReadTimeoutError:
                retry_count+=1
                sleep(self.RETRY_WAIT * retry_count)
