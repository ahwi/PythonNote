# celery

参考资料：

* 官方文档：https://docs.celeryq.dev/en/stable/



## Getting Started

### First Steps with Celery

本章学习：

* 选择和安装消息传输中间件（broker）
* 安装celery并创建第一个task
* 启动worker和调用tasks
* 跟踪任务在不同状态之间的转换，并检查返回值

#### 选择broker

#### 安装celery

#### Application

创建一个celery实例app，他是celery的入口，可以用它来创建tasks和管理worker等。

> 这边用单独一个脚本演示，工程化代码可以参考`https://docs.celeryq.dev/en/stable/getting-started/next-steps.html#project-layout`

创建第一个代码`tasks.py`

```python
from celery import Celery

app = Celery("tasks", broker="pyamqp://testUser:testUser@localhost:5672/testCelery")


@app.task
def add(x, y):
    return x + y
```

* Celery的第一个参数是当前模块的名称。这只是为了在`__main__`模块中定义任务时可以自动生成名称。

* 第二个参数是连接broker的，这边选择用rabbitmq做为broker

#### 启动celery的woker

使用如下命令：

```bash
celery -A tasks worker --loglevel=INFO
```

* 想要后台执行可以参考[supervisord](http://supervisord.org/) (see [Daemonization](https://docs.celeryq.dev/en/stable/userguide/daemonizing.html#daemonizing) for more information).

* 查看完整的命令：

  ```bash
  celery worker --help
  或
  celery --help
  ```


* celery在windows系统对多进程的支持有问题，可以通过`-P threads` 使用线程的方式来运行。

#### 调用任务

```python
>>> from tasks import add
>>> add.delay(4, 4)
```

>  `delay()`是`apply_async()`的快捷调用方式，可以更好的控制任务执行（详情查看 [Calling Tasks](https://docs.celeryq.dev/en/stable/userguide/calling.html#guide-calling)）

执行完上面的代码，任务就已经开始执行了，worker所在的控制台会有相应的输出。

调用任务后会有返回一个[AsyncResult](https://docs.celeryq.dev/en/stable/reference/celery.result.html#celery.result.AsyncResult)的实例。可以通过它来：

* 检查任务的状态
* 等待任务完成
* 获取返回值（如果任务失败，可以查看`exception`和`traceback`）

想要获取结果需要配置`结果后端(result backend)`

#### 保存结果

如果想要追踪任务的状态，celery需要有个地方用来保存或者发送状态。

celery有一些内置的`结果后端(result backend)`可供选择：

* [SQLAlchemy](http://www.sqlalchemy.org/)/[Django](http://djangoproject.com/) ORM
* [MongoDB](http://www.mongodb.org/)
* [Memcached](http://memcached.org/)
* [Redis](https://redis.io/)
* [RPC](https://docs.celeryq.dev/en/stable/userguide/configuration.html#conf-rpc-result-backend) ([RabbitMQ](http://www.rabbitmq.com/)/AMQP)
* 或者你可以自定义自己的结果后端

本例中，使用rpc作为结果后端，它将状态作为瞬时消息发送回来。

结果后端可以通过Celery的参数`backend`来指定（或者在configuration模块中的`result_backend`设置指定）。

如下：

* 在`task.py`中添加如下配置，就可以使用rabbitmq作为结果后端

  ```python
  app = Celery('tasks', backend='rpc://', broker='pyamqp://')
  ```

* 或者你可以使用Redis作为结构后端，然后还是使用rabbitmq来作为消息代理（比较流行的组合）

  ```python
  app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')
  ```

更多内容可以参考[Result Backends](https://docs.celeryq.dev/en/stable/userguide/tasks.html#task-result-backends)。

使用控制台导入tasks执行任务

```python
>>> from tasks import add    # close and reopen to get updated 'app'
>>> result = add.delay(4, 4)
```

`ready()`用来返回任务是否完成

```python
>>> result.ready()
False
```

你可以等待任务完成（但是这个很少使用，因为这把异步调用的变成同步调用了）

```python
>>> result.get(timeout=1)
8
```

当任务执行异常时，`get()`会重新发送异常，当可以通过propagate参数来覆盖此属性，下面对比有无使用`propagate`参数的效果：

* 没有指定`propagate`时，task任务执行异常：

  ```bash
  >>> result.get()
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\celery\result.py", line 220, in get
      self.maybe_throw(callback=callback)
    File "C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\celery\result.py", line 336, in maybe_throw
      self.throw(value, self._to_remote_traceback(tb))
    File "C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\celery\result.py", line 329, in throw
      self.on_ready.throw(*args, **kwargs)
    File "C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\vine\promises.py", line 234, in throw
      reraise(type(exc), exc, tb)
    File "C:\Users\Administrator\AppData\Local\Programs\Python\Python37\lib\site-packages\vine\utils.py", line 30, in reraise
      raise value
  ZeroDivisionError: division by zero
  >>>
  ```

* 指定`propagate`时：

  ```python
  >>> result.get(propagate=False)
  ZeroDivisionError('division by zero')
  >>> 
  ```

可以访问原始的`traceback`

```bash
>>> result.traceback
'Traceback (most recent call last):\n  File "c:\\users\\administrator\\appdata\\local\\programs\\python\\python37\\lib\\site-packages\\celery\\app\\trace.py", line 451, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File "c:\\users\\administrator\\appdata\\local\\programs\\python\\python37\\lib\\site-packages\\celery\\app\\trace.py", line 734, in __protected_call__\n    return self.run(*args, **kwargs)\n  File "E:\\15.note\\02.language\\01.python\\code\\utils\\celeryLearn\\01\\firstStep\\tasks.py", line 8, in add\n    1/0\nZeroDivisionError: division by zero\n'
>>>
```

> warning:
>
> 后端使用资源来存储和传输结果。为了确保释放资源，您最终必须在调用任务后返回的每个AsyncResult实例上调用get()或forget()。
>
> （测试forget()用不了，不确定什么原因导致）

完整的结果对象引用查看[`celery.result`](https://docs.celeryq.dev/en/stable/reference/celery.result.html#module-celery.result) 

#### 配置

暂时略过

https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#id12

## User Guide

### Application

Celery在使用之前必须初始化实例，该实例我们称作`application`（或`app`）

该应用程序是线程安全的，因此具有不同配置、组件和任务的多个Celery应用程序可以在同一进程空间中共存。

创建一个app实例:

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__ at 0x20f2f325088>
```

最后一行的信息包括：

* app类的名字：`Celery`
* 当前main模块的名字：`__main__`
* 实例的内存地址：`0x20f2f325088`

#### Main Name

当你发送一个任务消息给celery，该消息不会包含任何源代码，只包含了你想执行的任务的名称。每个woker都维护一个`task registry（任务注册表）`，包含任务名称到实际函数的映射。

当你定义一个task时，该任务会被加入到`local register(本地注册表)`上：

```python
>>> from celery import Celery
>>> app = Celery()
>>> @app.task
... def add(x, y):
...     return x + y
...
>>> add
<@task: __main__.add of __main__ at 0x20f2f325088>
>>> add.name
'__main__.add'
>>> app.tasks['__main__.add']
<@task: __main__.add of __main__ at 0x20f2f325088>
>>> quit()
```

这里又看到了`__main__`；每当Celery无法检测到函数所属的模块时，它会使用主模块名称来生成任务名称的开头。

This is only a problem in a limited set of use cases:

1. If the module that the task is defined in is run as a program.
2. If the application is created in the Python shell (REPL).

例如，使用`app.worker_main()`启动tasks模块中的worker：

`tasks.py`

```python
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == "__main__":
    app.worker_main()
```

当执行此模块时，tasks的命名会以`__main__`开头，但是当模块被其他程序导入时，该tasks的命名会以`tasks`（模块的真实名称）为开头：

```python
Type "help", "copyright", "credits" or "license" for more information.
>>> from tasks import add
>>> add.name
'tasks.add'
>>> quit()
```

你也可以给它指定一个名称：

```python
>>> from celery import Celery
>>> app = Celery('testTasks')
>>> app.main
'testTasks'

>>> @app.task
... def add(x, y):
...     return x + y

>>> add.name
'testTasks.add'
```

> 详情参考：
>
>  Names: https://docs.celeryq.dev/en/stable/userguide/tasks.html#task-name

