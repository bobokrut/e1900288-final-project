from dotenv import load_dotenv
from os import environ

load_dotenv()
DATABASE_URL = environ.get("DATABASE_URL")  # in Heroku this variable is always presenting
SECRET_KEY = environ.get("SECRET_KEY")
