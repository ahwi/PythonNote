# RabbitMQ



## 参考:

<https://blog.csdn.net/hellozpc/article/details/81436980#RabbitMQ_14>

<https://www.zhihu.com/people/zi-ji-47-82/posts?page=2>

一些rabblitMQ的入门概念:

<https://blog.csdn.net/lyhkmm/article/details/78775369>



## 安装:

1. 安装Erlang
2. 安装RabbitMQ

## 开始:

### 1. 启动:

   1. 启动 RabbitMQ Command Prompt管理工具

   2. 执行如下命令:

      ```
      rabbitmq-plugins enable rabbitmq_management
      ```

   3. 命令:

     ```
     停止：net stop RabbitMQ
     启动：net start RabbitMQ
     ```
   4. 访问管理页面: 

      http://127.0.0.1:15672/ 默认账号: guest/ guest

#### 1.1添加用户:

1. 用户角色:

   1、超级管理员(administrator)
   可登陆管理控制台，可查看所有的信息，并且可以对用户，策略(policy)进行操作。
   2、监控者(monitoring)
   可登陆管理控制台，同时可以查看rabbitmq节点的相关信息(进程数，内存使用情况，磁盘使用情况等)
   3、策略制定者(policymaker)
   可登陆管理控制台, 同时可以对policy进行管理。但无法查看节点的相关信息(上图红框标识的部分)。
   4、普通管理者(management)
   仅可登陆管理控制台，无法看到节点信息，也无法对策略进行管理。
   5、其他
   无法登陆管理控制台，通常就是普通的生产者和消费者。

2. 添加admin用户:

   ![1574735894537](assets/1574735894537.png)

### 1.2 创建Virtual Hosts

TODO



### 1.3 管理界面中的功能

![1574736382681](assets/1574736382681.png)

![1574736400729](assets/1574736400729.png)



### 2. 学习五种队列

![1574736500514](assets/1574736500514.png)



## 学习官网:

<https://www.rabbitmq.com/getstarted.html>

### 0. 简介

**rabbitMQ:** message broker（消息代理） --> 用来接收并转发消息 

概念:

* Producer：发送消息的程序
* queue：
  * 存储消息的盒子，消息流经rabbitmq和应用程序，但是只能存储在队列中。
  * 多个生产者可以发送到同一个队列，多个消费者也可以从队列中取消息
* consumer: 消息接收者

producer、consumer、broker不需要再同一台主机上面

### 1. hello world

#### 1. 使用pika python客户端

* 安装:

```python
python -m pip install pika
```

#### 2. 发送：

​	![1574844441637](assets/1574844441637.png)

send.py: 发送一个"hello"字符串到队列中

```python
import pika

# 1. 跟rabbitMQ建立连接
connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 2. 确保消息队列存在 注:如果消息队列不存在，rabbitMQ只是简单的将消息丢弃
channel.queue_declare(queue='hello')
# 3. 消息需要通过exchange才能到达队列，传递空字符串可以使用默认的exchange
channel.basic_publish(
        exchange='',
        routing_key='hello',
        body='Hello World!'
        )
print("[x] Sent 'Hello World!'")
# 4. 在退出程序之前，需要确保网络缓冲区已经刷新并且我们的消息已经投递到rabbitMQ中，这可以通过简单的关闭连接来实现
connection.close()
```

receive.py：从队列中接收消息并打印到屏幕

```python
import pika

# 1. 跟rabbitMQ建立连接
connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 2. 确保消息队列存在。不管执行多少次，队列只会被创建一次
channel.queue_declare(queue='hello')

# 3. 定义回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始循环等待消息的到来
channel.start_consuming()
```

查看当前的消息数:

```cmd
# linux:
$ sudo rabbitmqctl list_queues
# Windows:
$ rabbitmqctl.bat list_queues
```



### 2. work queue

![1574846883006](assets/1574846883006.png)

在这一部分中，我们将创建一个工作队列，该队列将用于在多个工作人员之间分配耗时的任务





### 问题

1. topic 如果客户端（接收消息的程序）不存在，发送的消息会被简单的丢弃，发送端怎么确认消息是否被发送

