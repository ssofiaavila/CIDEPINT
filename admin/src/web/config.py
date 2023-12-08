from os import environ

class Config(object):
    """Base Configuration
    """
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    
    
class ProductionConfig(Config):
    """Production Configuration
    """
    
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST =  environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )

    
class DevelopmentConfig(Config):
    """Development Configuration
    """
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST =  environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
  
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )

class TestingConfig(Config):
    """Development Configuration
    """
    TESTING = True
    
    

config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "test" : TestingConfig
}

google_oAuth_url = {
    "development" : "http://localhost:5000",
    "production" : "https://admin-grupo19.proyecto2023.linti.unlp.edu.ar",
    "test" : "http://localhost:5000"
}