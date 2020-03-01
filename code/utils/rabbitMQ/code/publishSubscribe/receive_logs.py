import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 创建一个类型为fanout的exchange,名字叫做"logs"
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 让服务器帮我们创建一个随机名称的队列;设置exclusive独占标志，当连接断开时，队列会被删除
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 绑定exchange和queue，让exchange接收到消息时可以发送给队列
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
