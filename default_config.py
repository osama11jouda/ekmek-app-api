import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # "sqlite:///data.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
SECRET_KEY = os.environ.get("APP_SECRET_KEY")

UPLOADED_IMAGES_DEST = os.path.join('static', 'images')