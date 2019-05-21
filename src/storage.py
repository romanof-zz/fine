import io
import os
import boto3

class S3Storage:
    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.bucket = bucket

    def put(self, key, data):
        obj = self.s3.Object(self.bucket, key)
        obj.put(Body=data)

    def get(self, key):
        obj = self.s3.Object(self.bucket, key)
        return obj.get()['Body'].read().decode('utf-8')
