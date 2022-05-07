from dotenv import load_dotenv
from os import environ, path

load_dotenv()

if not environ.get("DATABASE_URL"):
    raise NameError("DATABASE_URL is not defined")

if not environ.get("SECRET_KEY"):
    raise NameError("DATABASE_URL is not defined")

DATABASE_URL: str = environ.get("DATABASE_URL")  # type: ignore # in Heroku this variable is always presenting
SECRET_KEY: str = environ.get("SECRET_KEY")  # type: ignore
IMAGES_FOLDER: str = path.join(path.dirname(__file__), "static", "gallery", "images")
THUMBS_FOLDER: str = path.join(path.dirname(__file__), "static", "gallery", "thumbs")
