from celery import Celery

app = Celery("tasks", backend='rpc://', broker="pyamqp://testUser:testUser@localhost:5672/testCelery")


@app.task
def add(x, y):
    # 1/0 # test exception
    return x + y
