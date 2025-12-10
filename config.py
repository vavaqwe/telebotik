from dotenv import load_dotenv
import logging
import os

load_dotenv()

TELEGRAM_API = os.environ.get('TELEGRAM_API')
DATABASE = os.environ.get('DATABASE')
LOG_FILE = os.environ.get('LOG_FILE')
SECRET = os.environ.get('SECRET')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

logging.basicConfig(level=logging.INFO,
					filename=LOG_FILE,
					filemode="w",
					encoding='utf-8',
					format="%(asctime)s %(levelname)s %(message)s")
