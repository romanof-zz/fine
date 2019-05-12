import os
import boto3

class S3CachedStore:
    def __init__(self, root):
        self.s3 = boto3.client('s3')
        self.cache_root = "{dir}/.cache/".format(dir=root)

    def with_bucket(self, bucket):
        self.bucket = bucket
        self.bucket_cache_root = self.cache_root + bucket
        return self

    def put(self, key, data):
        with open(self.__cached_path(key), 'wb') as file:
            file.write(data)
            self.s3.upload_fileobj(file, self.bucket, key)

    def get(self, key):
        try:
            file = open(self.__cached_path(key), 'r')
            return file
        except FileNotFoundError:
            if not os.path.isdir(self.bucket_cache_root):
                os.mkdir(self.bucket_cache_root)

            with open(self.__cached_path(key), 'wb') as file:
                self.s3.download_fileobj(self.bucket, key, file)

            file = open(self.__cached_path(key), 'r')
            return file

    def __cached_path(self, key):
        return "{}/{}".format(self.bucket_cache_root, key)
