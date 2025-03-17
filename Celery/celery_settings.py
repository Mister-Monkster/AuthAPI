import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()


# os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")


celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@localhost:5672//",
    backend="rpc://",
    include=['Celery.tasks']
)


celery_app.conf.update(
    SMTP_HOST=os.getenv("SMTP_HOST"),
    SMTP_PORT=int(os.getenv("SMTP_PORT")),
    SMTP_USER=os.getenv("SMTP_USER"),
    SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
)

