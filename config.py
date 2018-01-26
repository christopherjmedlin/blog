import os

class Config():
    """
    Base configuration
    """
    MONGO_URI = os.environ.get("MONGO_URI", 
        "mongodb://user:password@localhost:27017")

class DevelopmentConfig(Config):
    """
    Configurations for development and testing
    """
    DEBUG = True

    SECRET_KEY = "?UWyue['(R0pM.9(v/Y=U_lJNn*ClO"

    # placeholder blog title for development
    BLOG_TITLE = "Blog"
    
class ProductionConfig(Config):
    """
    Configurations for production and staging
    """
    DEBUG = False

    # flask-s3 stuff
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    FLASKS3_BUCKET_NAME = "blog-files"
    FLASKS3_REGION = "us-west-2"

    # BLOG_TITLE = "my_blog"