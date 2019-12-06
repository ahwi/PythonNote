import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 这里需要和发送端保持一致（习惯和要求）
channel.exchange_declare(exchange='logs',
exchange_type='fanout')

# 类似的，比如log，我们其实最想看的，当连接上的时刻到消费者退出，这段时间的日志
# 有些消息，过期了的对我们并没有什么用
# 并且，一个终端，我们要收到队列的所有消息，比如：这个队列收到两个消息，一个终端收到一个。
# 我们现在要做的是：两个终端都要收到两个
# 那么，我们就只需做个临时队列。消费端断开后就自动删除
result = channel.queue_declare('', exclusive=True)
# 取得队列名称
queue_name = result.method.queue

# 将队列和交换机绑定一起
channel.queue_bind(exchange='logs',
queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body}")


# no_ack=True:此刻没必要回应了
channel.basic_consume(on_message_callback=callback,
queue=queue_name,
auto_ack=True)

channel.start_consuming()
