import os
import unittest

class Config():
    """
    Base configuration
    """

    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", None)
    MONGO_DB_USER = os.environ.get("MONGO_DB_USER", None)
    MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD", None)
    MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST", None)
    MONGO_DB_PORT = os.environ.get("MONGO_DB_PORT", None)

    BLOG_TITLE = os.environ.get("BLOG_TITLE", "Blog")
    SECRET_KEY = os.environ.get("SECRET_KEY", "?UWyue['(R0pM.9(v/Y=U_lJNn*ClO")

    TEST_RUNNER = unittest.TextTestRunner()

    # flask-s3 stuff
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    FLASKS3_BUCKET_NAME = "blog-christophermedlinme-static"
    FLASKS3_CDN_DOMAIN = "d1hw50uwx6u0j3.cloudfront.net"
    FLASKS3_REGION = "us-west-2"

class DevelopmentConfig(Config):
    """
    Configurations for development and testing
    """
    DEBUG = True
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/test")
    
class ProductionConfig(Config):
    """
    Configurations for production and staging
    """
    DEBUG = False
    PROTOCOL = os.environ.get("PROTOCOL", "http")
    MONGO_URI = os.environ.get("MONGO_URI", None)