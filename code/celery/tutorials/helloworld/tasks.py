from celery import Celery

broker_url = 'amqp://testUser:testUser@localhost:5672/celery'
backend_url = 'rpc://'
app = Celery('tasks',  backend=backend_url, broker=broker_url,)

@app.task
def add(x, y):
    return x + y