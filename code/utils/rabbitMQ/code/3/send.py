import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 原则上，消息，只能有交换机传到队列。就像我们家里面的交换机道理一样。
# 有多个设备连接到交换机，那么，这个交换机把消息发给那个设备呢，就是根据
# 交换机的类型来定。类型有：direct\topic\headers\fanout
# fanout：这个就是，所有的设备都能收到消息，就是广播。
# 此处定义一个名称为'logs'的'fanout'类型的exchange
channel.exchange_declare(exchange='logs',
exchange_type='fanout')

# 将消息发送到名为log的exchange中
# 因为是fanout类型的exchange，所以无需指定routing_key
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs',
routing_key='',
body=message)
print(" [x] Sent %r" % message)
connection.close()
