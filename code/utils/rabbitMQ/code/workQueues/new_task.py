import pika
import sys


connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
channel = connection.channel()

# durable: 声明队列为持久化队列
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World"
channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        # delivery_mode=2: 将消息设置为持久化消息
        properties=pika.BasicProperties(
            delivery_mode=2,)  # make message persistent
        )
print("[x] Sent 'Hello World!'")
connection.close()
