from celery import Celery

app = Celery("tasks", broker="pyamqp://testUser:testUser@localhost:5672/testCelery")


@app.task
def add(x, y):
    return x + y
