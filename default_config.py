import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = "postgresql://pytkniirytqjxc:89c62818f4a189a2429b2451b5cbe8b2deb4c9b729f64a1222b556a1e422287c@ec2-52-19-96-181.eu-west-1.compute.amazonaws.com:5432/d9n0em3nsumcvp"# os.environ.get("DATABASE_URL")  # "sqlite:///data.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
SECRET_KEY = os.environ.get("APP_SECRET_KEY")

UPLOADED_IMAGES_DEST = os.path.join('static', 'images')
