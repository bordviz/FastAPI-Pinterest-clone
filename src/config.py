from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

SECRET = os.environ.get('SECRET')
REFRESH_SECRET = os.environ.get('REFRESH_SECRET')
ALGORITHM = os.environ.get('ALGORITHM')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

EMAIL_SEND = os.environ.get('EMAIL_SEND')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

IMAGE_PLACEHOLDER = os.environ.get('IMAGE_PLACEHOLDER')