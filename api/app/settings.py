import os
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
	class DB:
	    HOST: str = os.getenv('TA_HOST')
	    PORT: str = os.getenv('TA_PORT')
	    DB: str = os.getenv('TA_DATABASE')
	    USER: str = os.getenv('TA_USER')
	    PASSWORD: str = os.getenv('TA_PASSWORD')

	class Clasifier:
	    MODEL_PATH: str = os.getenv('TA_MODEL_PATH')
	    CONF: float = 1/100

templates = Jinja2Templates(directory="templates")

settings: Settings = Settings()
