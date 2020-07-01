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


# 第四章：迭代器与生成器
## 4.1 手动遍历迭代器
不使用for循环而使用next()来手动遍历迭代器，`StopIteration`指示迭代器的结尾

```python

def manual_iter(filename):
    with open(filename) as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass


def main():
    filename = r""
    manual_iter2(filename=filename)

if __name__ == "__main__":
    main()
```



## 4.2 代理迭代
问题： 想要迭代自定义容器类，里面使用的是列表、元祖或其他可迭代对象作为容器，可以使用代理迭代。
解决方法：定义一个`__iter__()`方法，将迭代操作代理到容器内部的对象上去，比如：
```python
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return "Node({!r})".format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)



def main():
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)

if __name__ == "__main__":
    main()
```

`__iter__()`只是简单的将迭代请求传递给内部的`_children`属性

讨论:

* python的迭代协议需要`__iter__()`方法返回一个实现了`__next__()`方法的迭代器对象。

* `iter(s)`：调用`s.__iter__()`方法来返回对应的迭代器对象。


# 第六章：数据编码和处理

## 6.1读写csv数据
### 问题：
你想读写一个cvs格式的文件

### 解决方案：

**可以使用<font color=red>csv</font>库:**

例如：假设你在一个名叫stocks.csv文件中有一些股票市场数据，就像这样：

```cvs
Symbol,Price,Date,Time,Change,Volume
"AA",39.48,"6/11/2007","9:36am",-0.18,181800
"AIG",71.38,"6/11/2007","9:36am",-0.15,195500
"AXP",62.58,"6/11/2007","9:36am",-0.46,935000
"BA",98.31,"6/11/2007","9:36am",+0.12,104800
"C",53.08,"6/11/2007","9:36am",-0.25,360900
"CAT",78.29,"6/11/2007","9:36am",-0.23,225400
```

将这些数据读取为一个元组的序列：

```python
def read_csv():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        for row in f_csv:
            print(row)
```



**使用命名元祖来访问：**

```python
def read_csv_namedtuple():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        Row = namedtuple('Row', headers)
        for r in f_csv:
            row = Row(*r)
            print(row.Symbol)
```

它允许你使用列名如 <font color=red>row.Symbol</font>和 <font color=red>row.Change</font> 代替下标访问。需要注意的是这个只有在列名是合法的Python标识符的时候才生效。如果不是的话， 你可能需要修改下原始的列名(如将非标识符字符替换成下划线之类的)。



**将数据读取到一个字典序列中：**

```python
def read_csv_dict():
    with open('stocks.csv', 'r') as f:
        f_csv = csv.DictReader(f)
    	for row in f_csv:
            print(row['Symbol'])
```



**写入csv数据：**

仍然可以使用csv模块，不过这时候先创建一个<font color=red>writer</font>对象。例如：

```python
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
         ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
         ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]

with open('stocks.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
```

如果你有一个字典序列的数据，可以像这样做：

```python
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]

with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)
```



**讨论：**

csv产生的数据都是字符串类型的，它不会做任何其他类型的转换。 如果你需要做这样的类型转换，你必须自己手动去实现。

下面是一个在CSV数据上执行其他类型转换的例子：

```python
def read_csv_typeConversion():
    col_types = [str, float, str, str, float, int]
    with open('stocks.csv', 'r') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        for row in f_csv:
            # Apply conversions to the rows
            row = tuple(convert(value) for convert, value in zip(col_types, row))
            print(row)

# 打印信息：
['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800)
('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500)
('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000)
('BA', 98.31, '6/11/2007', '9:36am', 0.12, 104800)
('C', 53.08, '6/11/2007', '9:36am', -0.25, 360900)
('CAT', 78.29, '6/11/2007', '9:36am', -0.23, 225400)
```



最后，如果你读取CSV数据的目的是做数据分析和统计的话， 你可能需要看一看 `Pandas`包。`Pandas` 包含了一个非常方便的函数叫 `pandas.read_csv()` ， 它可以加载CSV数据到一个 `DataFrame` 对象中去。 然后利用这个对象你就可以生成各种形式的统计、过滤数据以及执行其他高级操作了




## 6.2 读写json数据
### 问题：

你想读写JSON(JavaScript Object Notation)编码格式的数据

### 解决方案：

<font color=red>json:</font> 字体 模块提供了一种很简单的方式来编码和解码JSON数据

**处理字符串，两个主要的函数：**

* <font color=red>json.dumps():</font>将一个Python数据结构转换为JSON
* <font color=red>json.loads():</font>将一个JSON编码的字符串转换回一个Python数据结构

* 例子：

  ```python
  # 将一个Python数据结构转换为JSON
  import json
  
  data = {
      'name' : 'ACME',
      'shares' : 100,
      'price' : 542.23
  }
  
  json_str = json.dumps(data)
  
  # 将一个JSON编码的字符串转换回一个Python数据结构
  data = json.loads(json_str)
  ```


**处理文件，两个主要的函数：**

* <font color=red>json.dumps()</font>
* <font color=red>json.loads()</font>

* 例子：

  ```python
  # Writing JSON data
  with open('data.json', 'w') as f:
      json.dump(data, f)
  
  # Reading data back
  with open('data.json', 'r') as f:
      data = json.load(f)
  ```

### 讨论：

**json编码支持的基本数据类型：**

* <font color=red>None, bool, int, float,str</font>

* 及包含这些数据类型的<font color=red>lists,tuples,dictionaries</font> （ 对于dictionaries，keys需要是字符串类型(字典中任何非字符串类型的key在编码时会先转换为字符串)）


**json编码的格式对于Python语法而已几乎是完全一样的:**

下面是一个例子，演示了编码后的字符串效果：

```python
>>> json.dumps(False)
'false'
>>> d = {'a': True,
...     'b': 'Hello',
...     'c': None}
>>> json.dumps(d)
'{"b": "Hello", "c": null, "a": true}'
>>>
```

**json的打印：**

可以考虑使用pprint模块的<font color=red>pprint()</font>函数来代替普通的<font color=red>print()</font>函数。它可以按照字母顺序并以一种更加美观的方式输出。

下面是一个演示如何漂亮的打印输出Twitter上搜索结果的例子:

```python
>>> from urllib.request import urlopen
>>> import json
>>> u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
>>> resp = json.loads(u.read().decode('utf-8'))
>>> from pprint import pprint
>>> pprint(resp)
{'completed_in': 0.074,
'max_id': 264043230692245504,
'max_id_str': '264043230692245504',
'next_page': '?page=2&max_id=264043230692245504&q=python&rpp=5',
'page': 1,
'query': 'python',
'refresh_url': '?since_id=264043230692245504&q=python',
'results': [{'created_at': 'Thu, 01 Nov 2012 16:36:26 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:14 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:13 +0000',
            'from_user': ...
            },
            {'created_at': 'Thu, 01 Nov 2012 16:36:07 +0000',
            'from_user': ...
            }
            {'created_at': 'Thu, 01 Nov 2012 16:36:04 +0000',
            'from_user': ...
            }],
'results_per_page': 5,
'since_id': 0,
'since_id_str': '0'}
>>>
```



**json解析成对象：**

通常，json解码会根据提供的数据创建dicts或lists。不过可以通过<font color=red>json.loads()</font>传递<font color=red>object_pairs_hook</font>或<font color=red>object_hook</font>参数，来<font color=red>创建其他类型的对象</font>。

例如，下面是演示如何解码JSON数据并在一个OrderedDict中保留其顺序的例子：

```python
>>> s = '{"name": "ACME", "shares": 50, "price": 490.1}'
>>> from collections import OrderedDict
>>> data = json.loads(s, object_pairs_hook=OrderedDict)
>>> data
OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])
>>>
```



下面是如何将一个JSON字典转换为一个Python对象例子：

````python
>>> class JSONObject:
...     def __init__(self, d):
...         self.__dict__ = d
...
>>>
>>> data = json.loads(s, object_hook=JSONObject)
>>> data.name
'ACME'
>>> data.shares
50
>>> data.price
490.1
>>>
````



**序列化：**

看不大懂，暂时先不研究


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