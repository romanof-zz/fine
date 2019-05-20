import io
import os
import boto3

class S3CachedStore:
    def __init__(self, bucket):
        self.s3 = boto3.client('s3')
        self.bucket = bucket

    def put(self, key, data):
        self.s3.upload_fileobj(io.BytesIO(data), self.bucket, key)
