import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = "postgresql:"# os.environ.get("DATABASE_URL")  # "sqlite:///data.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = "key1" # os.environ.get("JWT_SECRET_KEY")
SECRET_KEY = "key2"

UPLOADED_IMAGES_DEST = os.path.join('static', 'images')
