# 第一章：数据结构和算法



## 1.1 解压序列赋值给多个变量

### 问题：

现在有一个包含 N 个元素的元组或者是序列，怎样将它里面的值解压后同时赋值给 N 个变量？

### 解决方案：

任何的序列（或者是可迭代对象）可以通过一个简单的赋值语句解压并赋值给多个变量。 唯一的前提就是变量的数量必须跟序列元素的数量是一样的。

例子：

```python
>>> p = (4, 5)
>>> x, y = p
```

如果变量个数和序列元素的个数不匹配，会产生一个异常:

```python
>>> p = (4, 5)
>>> x, y, z = p
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ValueError: need more than 2 values to unpack
>>>
```

**这种解压赋值可以用在任何可迭代对象上面，而不仅仅是列表或者元组。 包括字符串，文件对象，迭代器和生成器。**

```python
>>> s = 'Hello'
>>> a, b, c, d, e = s
>>> a
'H'
>>> b
'e'
>>> e
'o'
>>>
```



**可以使用任意变量名去占位，丢弃不需要的变量：**

```python
>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
>>> _, shares, price, _ = data
>>> shares
50
>>> price
91.1
>>>
```

## 1.2 解压可迭代对象赋值给多个变量

### 问题

如果一个可迭代对象的元素个数超过变量个数时，会抛出一个 `ValueError` 。 那么怎样才能从这个可迭代对象中解压出 N 个元素出来？

## 解决方案

Python 的星号表达式可以用来解决这个问题：

```python
>>> *trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
>>> trailing
[10, 8, 7, 1, 9, 5, 10]
>>> current
3
```

有时候，你想解压一些元素后丢弃它们，你不能简单就使用 `*` ， 但是你可以使用一个普通的废弃名称，比如 `_` 或者 `ign` （ignore）:

```python
>>> record = ('ACME', 50, 123.45, (12, 18, 2012))
>>> name, *_, (*_, year) = record
>>> name
'ACME'
>>> year
2012
>>>
```





# 第十二章： 并发编程

## 12.1 启动与停止线程

### 问题：

你要为需要并发执行的代码创建/销毁线程

### 解决方案：

<font color=red>threading</font> 库可以在单独的线程中执行任何的在 Python 中可以调用的对象

例子：

```python
# Code to execute in an independent thread
import time
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create and launch a thread
from threading import Thread
t = Thread(target=countdown, args=(10,))
t.start()
```

* 创建好线程对象之后，程序不会理解执行，需要调用start()方法
* Python中的线程会在一个单独的系统级线程中执行（比如说一个 POSIX 线程或者一个 Windows 线程），这些线程将由操作系统来全权管理。

**操作：**

* 查询线程对象的状态：

  ```python
  if t.is_alive():
      print('Still running')
  else:
      print('Completed')
  ```

* 将一个线程加入到当前线程，并等待它终止：

  ```python
  t.join()
  ```

* 对于需要长时间运行的线程或者需要一直运行的后台任务，你应当考虑使用后台线程:

  ```python
  t = Thread(target=countdown, args=(10,), daemon=True)
  t.start()
  ```



你无法结束一个线程，无法给它发送信号，无法调整它的调度，也无法执行其他高级操作。如果需要这些特性，你需要自己添加。比如说，如果你需要终止线程，那么这个线程必须通过编程在某个特定点轮询来退出。你可以像下边这样把线程放入一个类中:

```python
class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(5)

c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
c.terminate() # Signal termination
t.join()      # Wait for actual termination (if needed)
```

### 讨论：

* 由于全局解释锁（GIL）的原因，Python 的线程被限制到同一时刻只允许一个线程执行这样一个执行模型。所以，Python 的线程更适用于处理I/O和其他需要并发执行的阻塞操作（比如等待I/O、等待从数据库获取数据等等），而不是需要多处理器并行的计算密集型任务。

* 有时你会看到下边这种通过继承 <font color=red>Thread</font> 类来实现的线程：

```python
from threading import Thread

class CountdownThread(Thread):
    def __init__(self, n):
        super().__init__()
        self.n = n
    def run(self):
        while self.n > 0:

            print('T-minus', self.n)
            self.n -= 1
            time.sleep(5)

c = CountdownThread(5)
c.start()
```

尽管这样也可以工作，但这使得你的代码依赖于 <font color=red>threading</font> 库，所以你的这些代码只能在线程上下文中使用。上文所写的那些代码、函数都是与 <font color=red>threading</font>库无关的，这样就使得这些代码可以被用在其他的上下文中，可能与线程有关，也可能与线程无关。比如，你可以通过 <font color=red>multiprocessing</font> 模块在一个单独的进程中执行你的代码：	

```python
import multiprocessing
c = CountdownTask(5)
p = multiprocessing.Process(target=c.run)
p.start()
```

再次重申，这段代码仅适用于 CountdownTask 类是以独立于实际的并发手段（多线程、多进程等等）实现的情况。



## 12.2 判断线程是否启动

### 问题：

你已经启动了一个线程，但是你想知道它是不是真的已经开始运行了。

### 解决方法：

使用<font color=red>Event</font>来协调线程

线程的一个关键特性是每个线程都是独立运行且状态不可预测。如果程序中的其他线程需要通过判断某个线程的状态来确定自己下一步的操作，这时线程同步问题就会变得非常棘手。为了解决这些问题，我们需要使用 `threading` 库中的 `Event` 对象。 `Event` 对象包含一个可由线程设置的信号标志，它允许线程等待某些事件的发生。在初始情况下，event 对象中的信号标志被设置为假。如果有线程等待一个 event 对象，而这个 event 对象的标志为假，那么这个线程将会被一直阻塞直至该标志为真。一个线程如果将一个 event 对象的信号标志设置为真，它将唤醒所有等待这个 event 对象的线程。如果一个线程等待一个已经被设置为真的 event 对象，那么它将忽略这个事件，继续执行。 下边的代码展示了如何使用 `Event` 来协调线程的启动：

```python
from threading import Thread, Event
import time

# Code to execute in an independent thread
def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

# Create the event object that will be used to signal startup
started_evt = Event()

# Launch the thread and pass the startup event
print('Launching countdown')
t = Thread(target=countdown, args=(10,started_evt))
t.start()

# Wait for the thread to start
started_evt.wait()
print('countdown is running')
```

当你执行这段代码，“countdown is running” 总是显示在 “countdown starting” 之后显示。这是由于使用 event 来协调线程，使得主线程要等到 `countdown()` 函数输出启动信息后，才能继续执行。

### 讨论：

<font color=red>Event:</font> event 对象最好单次使用。（尽管可以通过 `clear()` 方法来重置 event 对象，但是很难确保安全地清理 event 对象并对它重新赋值。很可能会发生错过事件、死锁或者其他问题（特别是，你无法保证重置 event 对象的代码会在线程再次等待这个 event 对象之前执行））

<font color=red>Condition:</font> 如果一个线程需要不停地重复使用 event 对象，你最好使用 `Condition` 对象来代替。

<font color=red>Semaphore:</font>event对象的一个重要特点是当它被设置为真时会唤醒所有等待它的线程。如果你只想唤醒单个线程，最好是使用信号量或者 `Condition` 对象来替代。



例子：

* 下面的代码使用 `Condition` 对象实现了一个周期定时器，每当定时器超时的时候，其他线程都可以监测到：

  ```python
  import threading
  import time
  
  class PeriodicTimer:
      def __init__(self, interval):
          self._interval = interval
          self._flag = 0
          self._cv = threading.Condition()
  
      def start(self):
          t = threading.Thread(target=self.run)
          t.daemon = True
  
          t.start()
  
      def run(self):
          '''
          Run the timer and notify waiting threads after each interval
          '''
          while True:
              time.sleep(self._interval)
              with self._cv:
                   self._flag ^= 1
                   self._cv.notify_all()
  
      def wait_for_tick(self):
          '''
          Wait for the next tick of the timer
          '''
          with self._cv:
              last_flag = self._flag
              while last_flag == self._flag:
                  self._cv.wait()
  
  # Example use of the timer
  ptimer = PeriodicTimer(5)
  ptimer.start()
  
  # Two threads that synchronize on the timer
  def countdown(nticks):
      while nticks > 0:
          ptimer.wait_for_tick()
          print('T-minus', nticks)
          nticks -= 1
  
  def countup(last):
      n = 0
      while n < last:
          ptimer.wait_for_tick()
          print('Counting', n)
          n += 1
  
  threading.Thread(target=countdown, args=(10,)).start()
  threading.Thread(target=countup, args=(5,)).start()
  ```

* 如果你只想唤醒单个线程，最好是使用信号量或者 `Condition` 对象来替代。考虑一下这段使用信号量实现的代码:

  ```python
  # Worker thread
  def worker(n, sema):
      # Wait to be signaled
      sema.acquire()
  
      # Do some work
      print('Working', n)
  
  # Create some threads
  sema = threading.Semaphore(0)
  nworkers = 10
  for n in range(nworkers):
      t = threading.Thread(target=worker, args=(n, sema,))
      t.start()
      
  
  >>> sema.release()
  Working 0
  >>> sema.release()
  Working 1
  >>>
  ```




## 12.3 线程间通信

### 问题：

你的程序中有多个线程，你需要在这些线程之间安全地交换信息或数据

### 解决方案：

**使用queue中的队列：**

从一个线程向另一个线程发送数据最安全的方式可能就是使用 <font color=red>queue</font> 库中的队列了。创建一个被多个线程共享的 <font color=red>Queue</font> 对象，这些线程通过使用 <font color=red>put()</font> 和 <font color=red>get()</font> 操作来向队列中添加或者删除元素，例如:

```python
from queue import Queue
from threading import Thread

# A thread that produces data
def producer(out_q):
    while True:
        # Produce some data
        ...
        out_q.put(data)

# A thread that consumes data
def consumer(in_q):
    while True:
# Get some data
        data = in_q.get()
        # Process the data
        ...

# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
```

<font color=red>Queue</font>对象已经包含了必要的锁，所以你可以通过它在多个线程间多安全地共享数据。 当使用队列时，协调生产者和消费者的关闭问题可能会有一些麻烦。一个通用的解决方法是在队列中放置一个特殊的值，当消费者读到这个值的时候，终止执行。例如：

```python
from queue import Queue
from threading import Thread

# Object that signals shutdown
_sentinel = object()

# A thread that produces data
def producer(out_q):
    while running:
        # Produce some data
        ...
        out_q.put(data)

    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)

# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Check for termination
        if data is _sentinel:
            in_q.put(_sentinel)
            break

        # Process the data
        ...
```

本例中有一个特殊的地方：消费者在读到这个特殊值之后立即又把它放回到队列中，将之传递下去。这样，所有监听这个队列的消费者线程就可以全部关闭了。