from os import environ, path

try:

    from dotenv import load_dotenv
    load_dotenv()

except ImportError:
    pass

if not environ.get("DATABASE_URL"):
    raise NameError("DATABASE_URL is not defined")

if not environ.get("SECRET_KEY"):
    raise NameError("SECRET_KEY is not defined")

DATABASE_URL: str = environ.get("DATABASE_URL")  # type: ignore #  NOTE: in Heroku this variable is always presenting
SECRET_KEY: str = environ.get("SECRET_KEY")  # type: ignore
IMAGES_FOLDER: str = path.join(path.dirname(__file__), "static", "gallery", "images")
THUMBS_FOLDER: str = path.join(path.dirname(__file__), "static", "gallery", "thumbs")
