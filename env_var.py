from dotenv import load_dotenv
from os import environ, path

load_dotenv()
DATABASE_URL = environ.get("DATABASE_URL")  # in Heroku this variable is always presenting
SECRET_KEY = environ.get("SECRET_KEY")
IMAGES_FOLDER = path.join(path.dirname(__file__), "static", "gallery", "images")
THUMBS_FOLDER = path.join(path.dirname(__file__), "static", "gallery", "thumbs")  
