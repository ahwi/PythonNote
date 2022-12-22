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

  

