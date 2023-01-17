from celery import Celery

app = Celery('proj',
             broker='amqp://testUser:testUser@localhost:5672/celery',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()