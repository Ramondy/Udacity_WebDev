import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode and silence notifications.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database

# DONE: TODO IMPLEMENT DATABASE URL
database_name = "fyyur"
database_user = os.getenv('DBUSER')
database_pw = os.getenv('DBPW')
database_host = os.getenv('DBHOST')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(database_user, database_pw, database_host, database_name)
# 'postgresql+psycopg2://postgres:uDacity$@localhost:5432/fyyur'