import os

from celery import Celery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from Celery.celery_settings import celery_app
from dotenv import load_dotenv
from redis import Redis
import random
from Celery.celery_settings import celery_app

load_dotenv()


@celery_app.task()
def send_mail(code: int, to_email: str, subject: str, text_type='plain'):
    try:
        text = f'Ваш код подтверждения: {code}'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = to_email[0]
        msg['From'] = celery_app.conf.SMTP_USER
        msg.attach(MIMEText(text, text_type))
        try:
            smtp_server = smtplib.SMTP_SSL(celery_app.conf.SMTP_HOST, int(celery_app.conf.SMTP_PORT))
            smtp_server.login(celery_app.conf.SMTP_USER, celery_app.conf.SMTP_PASSWORD)
            smtp_server.sendmail(celery_app.conf.SMTP_USER, to_email[0], msg.as_string())
            smtp_server.quit()
        except Exception as e:
            print(f"Ошибка: {str(e)}")
        redis_client = Redis(host="localhost", port=6379, db=0)
        redis_client.setex(name=f'{to_email[0]}', value=code, time=600)
        print("Email sent successfully!")
        return f"Email sent to {to_email}"
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return f"Failed to send email: {str(e)}"
