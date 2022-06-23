import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'Secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:////'+ os.path.join(basedir, 'auth.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSONIFY_MIMETYPE = 'application/json'