from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager: LoginManager = LoginManager()
db: SQLAlchemy = SQLAlchemy()
