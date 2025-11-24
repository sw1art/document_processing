from celery import Celery

app = Celery(
    "worker",
    broker="amqp://user:password@rabbitmq:5672//",
    backend="rpc://"
)

app.autodiscover_tasks(['worker.tasks'])
