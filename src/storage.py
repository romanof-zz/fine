import io
import os
import sys
import boto3
import pymysql

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
