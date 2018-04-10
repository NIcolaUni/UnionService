import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'postgresql://nicola:'+os.environ.get("PASS_DB")+'@localhost:5432/UnionService'
    SQLALCHEMY_TRACK_MODIFICATIONS = False