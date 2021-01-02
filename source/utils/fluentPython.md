# 流畅的python

## 第一部分 序幕

### 第1章 Python数据类型

#### 1.1 一摞Python风格的纸牌

概述：

通过实现一个纸牌类来展示`__getitem__`和`__len__`这两个特殊方法

示例1-1 一摞有序的纸牌

```python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                              for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


deck = FrenchDeck()
```

*  `namedtuple`：

   用来构建只有少数属性但是没有方法的对象

  ```python
  beer_card = Card('7', 'diamonds')
  print(beer_card)
  ```

* `__len__`方法提供的：

  * 使用`len()`函数查看有多少张牌

    ```python
    print(len(deck))
    ```

* `__getitem__` 方法提供的：

  * 抽取指定位置的纸牌，使用下标读取某个位置的纸牌

    ```python
    print(deck[0])
    print(deck[-1])
    ```

  * 随机抽取纸牌：使用random.choice从一个序列中随机选出一个元素

    ```python
    from random import choice
    print(choice(deck))
    print(choice(deck))
    print(choice(deck))
    ```

  * `__getitem__` 方法把[]操作交给了self._cards列表 所以支持自动切片操作

    ```python
    # 查看最上面3张
    print(deck[:3])
    # 只看牌面是A的牌
    print(deck[12::13])
    ```

  * 让对象变得可迭代

    ```python
    # 迭代
    for card in deck:
        print(card)
    
    # 反向迭代
    for card in reversed(deck):
        print(card)
    ```

  * 迭代通常是隐式的，如果没有实现`__contains__`方法，那么`in`运算符就会按照顺序做一次迭代搜索

    ```python
    print(Card('Q', 'hearts') in deck)
    print(Card('7', 'bearts') in deck)
    ```

  * 排序： 2最小、A最大； 黑桃 > 红桃 > 方块 > 梅花

    ```python
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
    
    
    def spades_high(card):
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]
    
    
    for card in sorted(deck, key=spades_high):
        print(card)
    ```


#### 1.2 如何使用特殊方法

**1. `__len__`和`len()`的区别以及调用逻辑：**

* 特殊方法的存在是为了被python解释器调用的，你自己并不需要去调用它

  也就是说没有`my_object.len()`这种写法，而应该使用`len(my_object)`。执行`len(my_object)`的时候，如果my_object是一个自定义对象，那么Python会自己去调用其中由你实现的`__len__`方法。

* 对于Python的内置类型，`CPython`会抄近路，使用跟高效的调用方法：

  对于内置类型，比如`list`、`str`、`bytearray`等，`CPython`会抄近路，`__len__`实际上会直接返回`PyVarObject`里的`obj_size`属性。`PyVarObject`是表示内存中长度可变的内置对象的C语言结构体，直接读取这个值比调用一个方法要快很多。

**2. 通过内置函数（len、iter、str等）来使用特殊方法是最好的选择**

​	这些内置函数不仅会调用特殊方法，通常还提供额外的好处，而且对于内置的类来说，它们的速度更快。（14.12节中有详细的例子）

##### 1.2.1 模拟数值类型

概述：使用一个二维向量类介绍6个特殊方法：

* `__init__`
* `__repr__`
* `__abs__`
* `__bool__`
* `__add__`
* `__mul__`

##### 1.2.2 字符串表示形式

**1. `repr`函数**

内置函数`repr`能把一个对象用字符串的形式表达出来以便辨认，它是通过`__repr__`这个特殊方法来得到一个对象的字符串表示形式的。

**2. `__repr__`和`__str__`的区别**

* `__repr__`所返回的字符串应该准确、无歧义，并且尽可能表达出如何用代码创建出这个被打印的对象
* `__str__`是在`str()`函数被使用，或是在用print函数打印一个对象的时候才会被调用的，并且它返回的字符串对终端用户更友好。
* 如果只想实现这两个特殊方法其中的一个，`__repr__`是更好的选择，因为如果一个对象没有`__str__`函数，而Python又需要调用它的时候，解释器会用`__repr__`作为替代。

##### 1.2.3 算术运算符

略

##### 1.2.4 自定义布尔值

**1. python判定一个值或对象是否为真的逻辑**

为了判定一个值x为真还是为假，Python会调用bool(x)，这个函数只能返回True或者False。默认情况下，对于自定义的类的实例总是被认为真的，除非这个类对`__bool__`或`__len__`函数有自己的实现。`bool(x)`的背后是调用`x.__bool__()`的结果；如果不存在`__bool__`方法，那么`bool(x)`会尝试调用`x.len()`，若返回0，则bool会返回False，否则返回True。

#### 1.3 特殊方法一览

见书P10

#### 1.4 为什么len不是普通方法

`len`之所以不是一个普通方法，是为了让Python自带的数据结构可以走后门，`abs`也是同理。但是多亏了它是特殊方法，我们也可以把`len`用于自定义数据类型。这种处理方式在保持内置类型的效率和保证语言一致性之间找到了一个平衡点。

































## 第五部分 流畅控制

### 第14章 可迭代的对象、迭代器和生成器

**迭代器模式：**扫描内存中放不下的数据集时，我们要找到一种惰性获取数据的方式，即按需一次获取一个数据项。

**生成器与迭代器：**

* python中使用`yield`关键字用于构造生成器
* 所有生成器都是迭代器，因为生成器完全实现了迭代器接口
* 区别：
  * 迭代器用于从集合中取出元素
  * 生成器用于“凭空”生成元素

**iter函数**

解释器需要迭代对象x时，会自动调用iter(x)

内置的iter函数的作用：

* 检查对象是否实现了`__iter__`方法，如果实现了就调用它，获取一个迭代器
* 如果没有实现`__iter__`方法，但实现了`__getitem__`方法，Python会创建一个迭代器，尝试按顺序（从索引0开始）获取迭代对象
* 如果尝试失败，python会抛`TypeError`异常，通常会提示`‘"C object is not iterable"`，其中C是目标对象所属的类

检查对象x是否可迭代：

* `abc.Iterable`类实现了`__subclasshook__`方法，可以使用它来检查对象是否可迭代，但是它没有考虑`__getitem__`

  ```python
  class Foo:
      def __iter__(self):
          pass
  issubclasss(Foo, abc.Iterable)
  f = Foo()
  isinstance(f, abc.Iterable)
  ```

* 直接使用`iter(x)`，如果对象不可迭代会抛`TypeError:'C' object is not iterable`的异常

序列可以迭代，因为它实现了`__getitem__`方法

#### 14.2 可迭代对象与迭代器的对比

**可迭代的对象和迭代器之间的关系：**

* python从可迭代的对象中获取迭代器
* 使用`iter`内置函数可以获取迭代器的对象

**标准的迭代器接口有两个方法：**

* `__next__`:

  返回下一个可用的元素，如果元素没了，抛出StopIteration异常

* `__iter__`:

  返回self，以便在应该使用可迭代对象（这里的可迭代对象应该指迭代器对象，跟可迭代的对象不是同一个东西）的地方使用迭代器，例如在for循环中

**迭代器接口的类关系：**

* 迭代器接口在`collections.abs.Iterator`抽象基类中制定

* `Iterable`和`Iterator`的关系

  ![1596853787233](assets/1596853787233.png)

**`Iterator`源码 ：**

```python
class Iterator(Iterable):
    __slots__ = ()

    @abstractmethod
    def __next__(self):
        raise StopIteration

    @classmethod
    def __subclasshook__(cls, C):
        if cls is MyIterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and
                any("__iter__" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented
```

检查对象x是否为迭代器最好的方式是调用`isinstance(x, abc.Iterator)`，得益于`Iterator.__subclasshook__`方法，即使对象x所属的类不是`Iterator`类的真是子类或虚拟子类，也能这样检查

**迭代器的定义：**

* 实现了`__next__`方法，返回序列中的下一个元素，如果没有元素了，就抛`StopIteration`异常
* python中的迭代器还实现了`__iter__`方法，因此迭代器也可以迭代



#### 14.3 Sentence类第2版：典型的迭代器

**使用迭代器模式实现Sentence类**

```python
import re
import reprlib

RE_WORD = re.compile("\w+")

class SentenceV2:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self


def test_sentence1():
    s = SentenceV2('"The time has come," the Walrus said')
    print(s)
    for word in s:
        print(word)


def main():
    test_sentence1()


if __name__ == '__main__':
    main()
```

**构建可迭代的对象和迭代器时经常出现的错误:**

* 混淆了二者，比如想把Sentence变成迭代器

* 两者的区别：
  * 迭代器对象有个`__iter__`方法，每次都实例化一个新的迭代器
  * 迭代器要实现`__next__`方法，返回单个元素，实现`__iter__`方法，返回迭代器本身

* 在可迭代的对象加入`__next__`方法是一种糟糕的想法，这是一种常见的反模式，违反了迭代器模式的用途

**迭代器模式的用途：**

* 访问一个聚合对象的内容而无需暴露它的内部表示
* 支持对聚合对象的多种遍历
* 为遍历不同的聚合结构提供一个统一的接口（即支持多态迭代）

#### 14.4 Sentence类第3版：生成器函数

之前的版本的Sentence类中，`__iter__`方法调用`SentenceIterator`类的构造方法创建一个迭代器并将其方法，现在使用生成器来替换迭代器类，所以这里的`__iter__`方法是生成器函数

```python
import re
import reprlib

RE_WORD = re.compile("\w+")

class SentenceV3:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
        return
```

`__iter__`方法是生成器函数，调用时会构建一个实现了迭代器接口的生成器对象，因此不用再定义`SentenceIterator`类

#### 14.5 Sentence类第4版：惰性实现

之前的版本都是将words全部生成在列表中，可以利用生成器，在需要的时候才生成对应的单词数据

`re.finditer`函数是`re.findall`函数的惰性版本，利用该函数可以将Sentence修改称惰性版本

#### 14.6 Sentence类第5版：生成器表达式

简单的生成器函数可以替换成生成器表达式

如以下的生成器函数可以替换成表达式：

```python
# ======生成器函数============
def __iter__(self):
    for match in RE_WORD.finditer(self.text):
        yield match.group()
# ======生成器表达式=================
def __iter__(self):
   return (match.group() for match in RE_WORD.finditer(self.text))
```

生成器表达式：

* 可以理解为列表推导的惰性版本，不会迫切地构建列表，而是返回一个生成器，按需惰性生成元素。

* 生成器表示是语法糖，完全可以替换成生成器函数，不过有时使用生成器表达式更便利。

#### 14.7 何时使用生成器表达式

* 生成器表达式是创建生成器的简洁语法，无需先定义函数再调用
* 生成器函数可以使用多个语句实现复杂的逻辑，也可以作为协程使用

#### 14.9 标准库中的生成器函数

略

#### 14.10 Python 3.3中新出现的语句：yield from

如果生成器函数需要产出了一个生成器生成的值，传统的解决方法是使用嵌套的for循环，可以利用`yield from`语法，将循环操作依次交给接收到的各个可迭代对象处理。

例程：

* 利用嵌套for循环的传统方法

  ```python
  def chain(*iterables):
      for i in iterables:
          for i in it:
              yield i
              
  s = "ABC"
  t = tuple(range(3))
  list(chain(s, t))
  # out: ["A","B","C",0,1,2]
  ```

* 使用`yield from`语法

  ```python
  def chain(*iterables):
      for i in iterables:
          yield from i
              
  s = "ABC"
  t = tuple(range(3))
  list(chain(s, t))
  # out: ["A","B","C",0,1,2]
  ```


#### 14.12 深入分析iter函数

* 在python中迭代对象x时会调用`iter(x)`

* `iter`函数还有一个用法：传入两个参数，使用常规的函数或任何可调用的对象创建迭代器。这样使用时，第一个参数必须是可调用的对象，用于不断调用（没有参数），产生各个值；第二个是哨符，当可调用对象返回这个值时，触发迭代器抛出`StopIteration`异常

  例子：

  ```python
  def d6():
      return randint(1，6)
  
  d6_iter = iter(d6, 1)
  for roll in d6_iter:
      print(roll)
  ```



#### 14.13案例分析：在数据库转换工具

略

### 第15章 上下文管理器和else块

#### 15.1 先做这个，再做那个：if语句之外的else块

for while 语句后面的else子句

#### 15.2 上下文管理器和with块

* 上下文管理器对象存在的目的是管理with语句

* with语句的目的是简化try/finally模式
* 上下文管理器协议包含`__enter__`和`__exit__`两个方法。
  * `with`语句开始运行时，会再上下文管理器对象上调用`__enter__`方法
  * `with`语句运行结束后，会在上下文管理器对象上调用`__exit__`方法，以次扮演finally子句的角色

例程1：with的使用方法：

```python
with open("mirror.py") as fp:
    src = fp.read(60)
```

注：执行with后面的表达式得到的结果是上下文管理器对象，不过，把值绑定到目标变量上（as子句）是在上下文管理器对象上调用`__enter__`方法的结果

as子句是可选的

例程2：上下文管理器类LookingClass上下文管理器的代码

```python
class LookingClass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        self.stdout.write = self.reverse_write
        return 'JABBERWOCKY'
    
    def reverse_write(self, text):
        self.original_write(text[::-1])
        
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True
```



### 第16章 协程

#### 16.2 用作协程的生成器的基本行为

协程的四个状态：

* GEN_CREATED

  等待开始执行

* GEN_RUNNING

  解释器正在执行

* GEN_SUSPENDED

  在yield表达式处暂停

* GEN_CLOSED

  执行结束

可以使用`inspect.getgeneratorstate(...)`函数确定处于何种状态

使用协程前需要预激协程：

* next(my_coro)
* my_coro.send(None)

#### 16.4 预激协程的装饰器

自定义一个coroutine装饰器来预激协程





## 第六部分 元编程

### 第19章 动态属性和特性

在python中：

**属性：** 数据的属性和处理数据的方法

**特性：** 在不改变类接口的前提下，使用<font color=red>存取方法（即读值方法和设值方法）修改数据属性</font>

**控制属性的访问权限/实现动态属性的api:** 

* 特性
* `__getattr__`和`__setattr__`计算属性

#### 19.1 使用动态属性转换数据

例程：使用的同台属性处理JSON格式数据源

数据源格式如下：




<details>
  <summary>代码</summary>

```json
{
	"Schedule": {
		"conferences": [{
			"serial": 115
		}],
		"events": [{
			"serial": 34505,
			"name": "Why Schools Don´t Use Open Source to Teach Programming",
			"event_type": "40-minute conference session",
			"time_start": "2014-07-23 11:30:00",
			"time_stop": "2014-07-23 12:10:00",
			"venue_serial": 1462,
			"description": "Aside from the fact that high school programming...",
			"website_url": "http://oscon.com/oscon2014/public/schedule/detail/34505",
			"speakers": [157509],
			"categories": ["Education"]
		}],
		"speakers": [{
			"serial": 157509,
			"name": "Robert Lefkowitz",
			"photo": null,
			"url": "http://sharewave.com/",
			"position": "CTO",
			"affiliation": "Sharewave",
			"twitter": "sharewaveteam",
			"bio": "Robert ´r0ml´ Lefkowitz is the CTO at Sharewave, a startup..."
		}],
		"venues": [{
			"serial": 1462,
			"name": "F151",
			"category": "Conference Venues"
		}]
	}
}
```
</details>


##### 19.1.1 使用动态属性访问json类数据 

定义一个`FrozenJSON`类，把一个JSON数据集转换成一个嵌套这FronzeJson对象、列表和简单类型的FrozenJSON对象

<details>
  <summary>代码</summary>

```python
from collections import abc


class FrozenJSON:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
```

</details>

##### 19.1.2 处理无效属性名
FrozenJSON类有个缺陷：没有对名称为python关键字的属性做特殊处理

添加如下处理:
```python
def __init__(self, mapping):
    self.__data = {}
    for key, value in mapping.items():
        if keyword.iskeyword(key):
            key += '_'
        self.__data[key] = value

```
还有个缺陷: 如果JSON对象中的键不是有效的Python标识符，也会遇到类似的问题:
```
>>> x = FrozenJSON({'2be:'or not'})
>>> x.2be
  File "<stdin>", line 1
    x.2be
  SyntaxError: invalid syntax
```
把无效字符编程有效的属性名不容易，有两个简单的解决方法:
* 抛出异常
* 把无效的键换成通用名称，如`attr_0`、`attr_1`等

为了简单起见，忽略这个问题

##### 19.1.3 使用__new__方法以灵活的方式创建对象

在python中，用于构建实例的是特殊方法`__new__`

* 类方法（使用特殊方法处理，不必使用`@classmethod`装饰器）

* `__new__`返回一个实例并作为第一个参数（即self）传给`__init__`方法

* `__new__`是构造方法，`__init__`初始化方法。

* 从`__new__`方法到`__init__`方法是最常见的，但不是唯一的。`__new__`方法也可以返回其他类的实例

* 构建对象过程的伪代码：

  ```python
  def object_maker(the_class, some_arg):
      new_object = the_class.__new__(some_arg)
      if isinstance(new_object, the_class):
          the_class.__init__(new_object, some_arg)
      return new_object
  
  # 下述两个语句的作用基本等效
  x = Foo('bar')
  x = object_maker(Foo, 'bar')
  ```

##### 19.1.4 使用shelve模块调整OSCON数据源的结构





​	
