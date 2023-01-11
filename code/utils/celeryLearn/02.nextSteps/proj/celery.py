from celery import Celery

app = Celery('proj',
             broker='pyamqp://testUser:testUser@localhost:5672/testCelery',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()