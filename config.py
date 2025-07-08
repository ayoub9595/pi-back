import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/parc_informatique'
    SQLALCHEMY_TRACK_MODIFICATIONS = False