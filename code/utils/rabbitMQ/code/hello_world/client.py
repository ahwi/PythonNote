import pika

# 连接服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 创建队列:有就不管,没有就创建
channel.queue_declare(queue='hello')

# 收到消息后的回调
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)


channel.basic_consume(on_message_callback=callback, 
        queue="hello", auto_ack=True)
print("[*] Watting for message.To exit press CTRL+C")
channel.start_consuming()
