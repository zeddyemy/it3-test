import os, secrets
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


## postgresql://postgres:zeddy@localhost:5432/robin_sale
class Config:
    # other app configurations
    SECRET_KEY = os.urandom(32)
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:zeddy@localhost:5432/trendit3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')\
        or 'postgresql://trendit3_toru_user:f8kA8XmbVNChw8z4dkuTFIrsEv0lAP13@dpg-cl83nff6e7vc73a2ec20-a.oregon-postgres.render.com/trendit3_toru'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_DIR = 'app/static'
    UPLOADS_DIR = 'app/static/uploads'
    
    # JWT configurations
    JWT_SECRET_KEY = "super-secret" # Change This
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Set to True in a production environment
    JWT_ACCESS_COOKIE_PATH = '/api/'
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = True
    
    # FlutterWave Configurations
    FLUTTER_INITIALIZE_URL = "https://api.flutterwave.com/v3/payments"
    FLUTTER_SECRET_KEY = "FLWSECK_TEST-42411bcec771ba0d9a6cfbb21c9a3ca1-X"
    FLUTTER_PUBLIC_KEY = "FLWPUBK_TEST-0db308be49b1ea25ba4e320ae778f04a-X"
    FLUTTER_SECRET_HASH = "42cf4e6d9d8c728003ae3361d5268c23"
    
    # mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'olowu2018@gmail.com'
    MAIL_PASSWORD = 'doyi bkzc mcpq cvcv'
    
    # Cloudinary configurations
    CLOUDINARY_CLOUD_NAME = "dcozguaw3"
    CLOUDINARY_API_KEY = "798295575458768"
    CLOUDINARY_API_SECRET = "HwXtPdaC5M1zepKZUriKCYZ9tsI"
