import os

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True
    DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
    FTP_STORAGE_LOCATION = 'ftp://pyconfr:pyconfr@localhost:21'

    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = 'minio'
    # AWS_SECRET_ACCESS_KEY = 'minio123'
    # AWS_STORAGE_BUCKET_NAME = 'default'
    # AWS_AUTO_CREATE_BUCKET = True
    # AWS_S3_ENDPOINT_URL = 'http://localhost:9000'

    # Testing
    INSTALLED_APPS: tuple = Common.INSTALLED_APPS + ('django_extensions',)

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase.sqlite',
        }
    }


class Testing(Common):
    DEBUG = True
    DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
    FTP_STORAGE_LOCATION = 'ftp://pyconfr:pyconfr@localhost:21'

    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = 'minio'
    # AWS_SECRET_ACCESS_KEY = 'minio123'
    # AWS_STORAGE_BUCKET_NAME = 'default'
    # AWS_AUTO_CREATE_BUCKET = True
    # AWS_S3_ENDPOINT_URL = 'http://localhost:9000'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'pyconfr.sqlite',
        }
    }
