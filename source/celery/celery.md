# Celery

## 开始（getting started）

### Celery的介绍

### Backends和Brokers

### Celery的第一步

### 下一步

#### 在应用中使用Celery

##### 项目

目录层级：

```txt
proj/__init__.py
	/celery.py
	/tasks.py
```

proj/celery.py

```python
from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='rpc://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
```

proj/tasks.py

```python
from .celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
```

##### 启动worker

启动worker:在项目(proj)的上级目录下执行命令

```bash
$ celery -A proj worker -l INFO
```

启动时打印的信息：

```txt
 -------------- celery@xxx-xxx v5.0.5 (singularity)
--- ***** -----
-- ******* ---- Windows-10-10.0.19041-SP0 2021-05-29 17:25:51
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         proj:0x25dc75655f8
- ** ---------- .> transport:   amqp://testUser:**@localhost:5672/celery
- ** ---------- .> results:     rpc://
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . proj.tasks.add
  . proj.tasks.mul
  . proj.tasks.xsum
```

日志信息说明：

* broker：指定连接broker的URL信息。也可以使用`-b`选项来指定

* concurrency：用于同时处理任务的预工作的进程数量。

  默认使用的是CUP核数量，也可以使用`celery worker -c`选项来指定数量。

* Events：可以让celery监控由worker触发的一些行为。监控程序有`celery events`和`Flower`（实时监控），详细可以阅读[任务管理指南](https://docs.celeryproject.org/en/stable/userguide/monitoring.html#guide-monitoring)

* Queues：work会从队列列表里消费任务。详细可以看[路由指南](https://docs.celeryproject.org/en/stable/userguide/routing.html#guide-routing)

可以查看完整的参数介绍

```bash
$ celery worker --help
```

选项的详细介绍查看[Worker指南](https://docs.celeryproject.org/en/stable/userguide/workers.html#guide-workers)

##### 停止worker

可以简单的使用`Control-c`来停止。详细的信号支持查看[Worker指南](https://docs.celeryproject.org/en/stable/userguide/workers.html#guide-workers)

##### 后台运行

有时候你想在后台运行worker，可以使用**celery multi**命令来启动一个或多个worker。详细可以查看[demonnization tutorial](https://docs.celeryproject.org/en/stable/userguide/daemonizing.html#daemonizing)

```bash
$ celery multi start w1 -A proj -l INFO
celery multi v4.0.0 (latentcall)
> Starting nodes...
    > w1.halcyon.local: OK
```

重启：

```bash
$ celery  multi restart w1 -A proj -l INFO
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64024
> Waiting for 1 node.....
    > w1.halcyon.local: OK
> Restarting node w1.halcyon.local: OK
celery multi v4.0.0 (latentcall)
> Stopping nodes...
    > w1.halcyon.local: TERM -> 64052
```

停止：

* 异步

    ```bash
    $ celery multi stop w1 -A proj -l INFO
    ```

* 同步

  ```bash
  $ celery multi stopwait w1 -A proj -l INFO
  ```


> 注：在windows上测试不能运行，提示不支持

##### `--app`参数

使用`--app`参数指定Celery app实例，以`module.path:attribute`的形式

如果只指定了包名，celery会尝试搜索app的实例。

使用`--app=proj`的解析顺序

1. 名字为`proj.app`
2. 名字为`proj.celery`
3. any attribute in the module `proj` where the value is a Celery application, or

如果上面都没发现，会尝试使用`proj.celery`：

4. 名为`proj.celery.app`
5. 名为`proj.celery.celery`
6. `Any attribute in the module `proj.celery` where the value is a Celery application`

通常包含单个模块的项目使用`proj:app`，大项目使用`proj.celery:app`

#### 任务的调用

#### 画布：设计工作流程

#### 路由

#### 远程控制

#### 时区

#### 优化

#### 现在做什么





### 资源



## User Guide

### Application

celery库使用前要定义一个实例，这个实例叫做application或者app

application是线程安全的，因此具有不同配置，组件和任务的多个Celery应用程序可以共存于同一进程空间中。

下面创建一个实例：

```python
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__ at 0x1de3df731d0>
```

#### Main Name

在celery中发送任务消息时，该消息将不包含任何源代码，而仅包含要执行的任务的名称。

#### Configuration

#### Laziness

#### Breaking the chain

#### Abstract Tasks

