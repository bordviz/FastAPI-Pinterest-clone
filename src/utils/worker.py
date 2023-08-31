from celery import Celery
from config import REDIS_HOST, REDIS_PORT, EMAIL_SEND, EMAIL_PASS, SMTP_HOST, SMTP_PORT
from auth.mail import get_email_template
import smtplib
from db.db import async_session_maker
from sqlalchemy import select
from models.user import User
import asyncio

celery = Celery(
    __name__, 
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}"
)

@celery.task
def send_email_code(username: str, user_email: str, code: int):
    email = get_email_template(username, user_email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(EMAIL_SEND, EMAIL_PASS)
        server.send_message(email)
