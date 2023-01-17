# 协程 & asyncio & 异步编程



## 3. 异步编程

### 3.3 await

await + 可等待对象（协程对象、Future、Task对象 ==> IO等待）

示例1：

```python
import asyncio


async def func():
    print("hello")
    response = await asyncio.sleep(2)
    return response

asyncio.run(func())
```

示例2：

```python
import asyncio


async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def func():
    print("执行协程函数内部代码")

    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后在继续往下执行。当前协程挂起时，事件循环可以执行其他协程（任务）
    response = await others()
    print("IO请求结束，结果为：", response)

asyncio.run(func())

```

示例3：

```python
import asyncio


async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def func():
    print("执行协程函数内部代码")

    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后在继续往下执行。当前协程挂起时，事件循环可以执行其他协程（任务）
    response1 = await others()
    print("IO请求结束，结果为：", response1)
    response2 = await others()
    print("IO请求结束，结果为：", response2)

asyncio.run(func())

```

await就是等待对象的值得到结果之后再继续向下走。

### 3.4 Task对象

> Tasks are used to schedule coroutines concurrently
>
> When a corotine is wrapped into a Task with functions like `asyncio.create_task()` the coroutine is automaically scheduled to run soon.

白话：在事件循环中添加多个任务的。

Tasks用于并发调度协程，通过`asyncio.create_task(协程对象)`的方式创建Task对象，这样可以让协程加入事件循环中等待被调用执行。除了使用`asyncio.create_task()`函数以外，还可以用低层级的`loop.create_task()`或`ensure_future()`函数。不建议手动实例化Task对象。

注意：`asyncio.create_task()`函数在Python3.7中加入。在Python3.7之前，可以改用低层级的`asyncio.ensure_future()`函数。

示例1：

```python
import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def main():
    print("main开始")

    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task1 = asyncio.create_task(func())

    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task2 = asyncio.create_task(func())
    
    print("main结束")

    # 当执行某个协程遇到IO操作时，会自动切换执行其他任务
    # 此处的await是等待相应的协程全部执行完毕并获取结果
    ret1 = await task1  # 会等task1返回值才继续往下执行下一条语句
    ret2 = await task2
    print(ret1, ret2)

asyncio.run(main())

```

示例2：

```python
import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def main():
    print("main开始")

    task_list = [
        # python3.8的asyncio.create_task 有个name参数，可以给task取名字
        asyncio.create_task(func()),
        asyncio.create_task(func())
    ]

    print("main结束")

    done, pending = await asyncio.wait(task_list, timeout=None)
    print(done)

asyncio.run(main())

```

示例3：（等效示例2，代码更简洁）

```python
import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


task_list = [
    func(),
    func()
]

done, pending = asyncio.run(asyncio.wait(task_list))
print(done)

```

### 3.5 asyncio.Future对象

> A `Future` is a special **low-level** awaitable object that represents an **eventual result** of an asynchronous operation.

Task继承Future对象，Task对象内部await结果的处理基于Future对象来的。

示例1：

```python
import asyncio


async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务（Future对象），这个任务什么都不干
    fut = loop.create_future()

    # 等待任务最终结果（Future对象），没有结果则会一直等下去
    await fut


asyncio.run(main())

```

示例2：

```python
import asyncio


async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result("666")


async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务（Future对象），这个任务什么都不干
    fut = loop.create_future()

    # 创建一个任务（Task对象），绑定了set_after函数，函数内部在2s之后，会给fut赋值。
    # 即手动创建future任务的结果，那么fut就可以结束了
    await loop.create_task(set_after(fut))

    # 等待任务最终结果（Future对象），没有结果则会一直等下去
    data = await fut
    print(data)


asyncio.run(main())

```

### 3.6 concurrent.futures.Future对象

使用线程池、进程池实现异步操作时用到的对象。

示例1：

```python
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor


def func(value):
    time.sleep(1)
    print(value)
    return 123


# 创建线程池
pool = ThreadPoolExecutor(max_workers=5)

# # 创建进程池
# pool = ProcessPoolExecutor(max_workers=5)


for i in range(10):
    fut = pool.submit(func, 1)
    print(fut)

```

以后写代码可能会存在交叉使用。

在异步编程时，遇到某个官方应用不支持异步操作时，可以用线程、进程做异步编程。

例如：crm项目80%都是基于协程异步编程 + MySQL（假设不支持协程），这时需要用线程、进程做异步编程。

示例2：

```python
import time
import asyncio
import concurrent.futures


def func1():
    # 某个耗时操作
    time.sleep(2)
    return "结果"


async def main():
    loop = asyncio.get_running_loop()
    # 1. Run in the default loop's executor(默认ThreadPoolExecutor)
    # 第一步：内部会线调用ThreadPoolExecutor的submit方法取线程池中申请一个线程去执行func1函数，
    #        并返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.wrap_future将concurrent.futures.Future对象包装为asyncio.Future对象，
    #        因为concurrent.future.Future对象不支持await语法，所以需要包装为asyncio.Future对象才能使用
    fut = loop.run_in_executor(None, func1)
    result = await fut
    print("default thread pool", result)

    # # 2. Run in a custom thread pool
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #     print("custom thread pool", result)
    #
    # # 3. Run in a custom process pool:
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #     print("custom process pool", result)


asyncio.run(main())

```

