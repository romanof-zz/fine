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

class SQLStorage:
    def __init__(self, logger, host, user, password, db_name):
        self.logger = logger
        try:
            self.conn = pymysql.connect(host, user=user, passwd=password, db=db_name, connect_timeout=5)
        except Exception as e:
            self.logger.error(e)
            sys.exit()

    def load(self, query):
        self.logger.debug(query)
        with self.conn.cursor() as cur:
            cur.execute(query)
            return [row for row in cur]

    def execute(self, query):
        self.logger.debug(query)
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
