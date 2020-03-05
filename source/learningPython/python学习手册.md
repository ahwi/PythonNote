# python学习手册





## 第一部分：使用入门

### 模块的导入和重载

* 使用import语句在第一次导入之后，其他相同的导入不会再执行，如果导入的源文件在第一条import语句发生改变，也不会重新导入。

* 想要重新导入可以使用reload模块，reload是一个函数:

  ```python
  from imp import reload
  reload(script)
  ```

* reload是不可传递的，重载一个模块的话指挥重载该模块，而不能够重载该模块所导入的任何模块



### 寻求帮助

```python
>>> s = 'aaaa'
>>> dir(s)
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
>>> help(s.replace)
Help on built-in function replace:

replace(...) method of builtins.str instance
    S.replace(old, new[, count]) -> str

    Return a copy of S with all occurrences of substring
    old replaced by new.  If the optional argument count is
    given, only the first count occurrences are replaced.
```



## 第二部分 类型和运算

### 第六章

#### 变量、对象和引用



### 第八章 列表与字典

#### 列表

L.appedn(X) 会在原地修改L

L+[X]会生成新的列表



#### 字典

列表是有序的对象集合，字典是无序的集合。



### 文件

使用eval可以把字符串转换成对象

用pickle存储python的原生对象

struct模块能够构造并解析打包的二进制数据



### python中的其他类型

#### 重复能够增加层次深度

两种方式的区别：

```python
>>> L = [4,5,6]
>>> X = L * 4
>>> Y = [L] * 4
>>> X
[4,5,6,4,5,6,4,5,6,4,5,6]
>>> Y
[[4,5,6],[4,5,6],[4,5,6],[4,5,6]]
```



### 第十八章 参数

<font color=red>python中a = a+b与a += b的不同：</font>

```
a = a + b
创建过程是：先创建的a+b的对象放入内存，然后变量a指向了a+b的对象，这事实上已经改变了a原本的指向，指向了新的地址。
a += b
创建过程是：把a原本指向内存地址的对象的值改变成了a+b，能不能改变取决于该对象的值能不能被改变。
对于可变对象类型和不可变对象类型有不同的结果：
可变对象类型：+=改变了原本地址上对象的值，不改变原本的指向地址；=则改变了原本的指向地址，创建了新的对象，并指向新的地址
不可改变对象类型：都是改变原本的指向地址，指向新创建的对象地址 
```

举例：下面两个程序获得的结果不一样

```python
def test_code(a):
    a += [4,5,6]


if __name__ == "__main__":
    # main()
    l = [1,2,3]
    test_code(l)
    print(l)
    
```

```python
def test_code(a):
    a = [4,5,6]


if __name__ == "__main__":
    # main()
    l = [1,2,3]
    test_code(l)
    print(l)

### 结果：
[1, 2, 3]
```

## 第五部分 模块

### 第21章 模块:宏伟蓝图

#### 导读

模块可以由两个语句和一个重要的内置函数进行处理

* import
* from
* imp.reload

将学习:

* reload
* \_\_name\_\_
* \_\_all\_\_
* 封装import
* 相对导入语法

#### 为什么使用模块

#### Python程序架构

#### import 如何工作

#### 模块搜索路径



### 第22章 某块代码编写基础

* import 
* from



1. 导入只发生一次

2. import和from是赋值语句

   1. import将整个模块对象赋值给一个变量名

   2. from将一个或多个变量名赋值给另一个模块中同名的对象，对可变对象修改会影响另一个地方的这个对象

      1. 例子: small.py

         ```python
         # small.py
         x = 1
         y = [1,2]
         ================
         >>from small import x, y
         >>x = 42
         >>y[0] = 42
         
         >>import small
         >>small.x
         1
         >>small.y
         可变对象被修改会影响另一个地方的这个对象
         ```


3. 以from赋值而来的变量名和其来源的文件之间没有联系，为了实际修改另一个文件中的变量名，必须使用import：

   ```python
   >> from small import x, y
   >> x = 42	# changes my x only
   
   >> import small
   >> small.x = 42 # changes x in other module
   ```


4. from总是把整个模块导入到内存中，无论是从这个文件中复制出多少个变量名，只加载模块文件的一部分是不可能的。

## 第六部分 类和OOP

### 第31章 类的高级主题

概览:

* 建立内置类型的子类
* 新式类的变化和扩展
* 静态方法
* 类方法
* 函数装饰器

#### 扩展内置类型

* 通过嵌入扩展类型
* 通过子类扩展类型

#### 新式类

python3.0所有的类都继承自object



### 第38章 装饰器

#### 什么是装饰器

装饰是为函数和类指定管理代码的一种方法

两种装饰器:

* 函数装饰器
* 类装饰器

作用:

* 管理调用和实例
* 管理函数和类

#### 基础知识

##### 函数装饰器

**用法**

函数装饰器自动执行如下的映射:

```python
@decorator
def F(arg):
	...
F(99)

=映射为=>
def F(arg):
   	...
F = decorator(F)
F(99)
```





##### 类装饰器

##### 装饰器嵌套

##### 装饰器参数

##### 装饰器管理函数和类



#### 编写函数装饰器

##### 跟踪调用

需要统计一个函数被调用的次数，并且针对每次调用打印跟踪信息，下面有两种解决方案：

* 使用函数装饰器的方式

  ```python
  class tracer1:
      def __init__(self, func):
          self.calls = 0
          self.func = func
  
      def __call__(self, *args):
          self.calls += 1
          print("call %s to %s" % (self.calls, self.func.__name__))
          self.func(*args)
  
  
  @tracer1
  def spam(a, b, c):
      print(a + b + c)
  def main():
      # spam(1, 2, 3)
      # spam(1, 2, 3)
      # spam(1, 2, 3)
  
  if __name__ == "__main__":
      main()
  
  ```

* 使用普通函数调用的方式

  ```python
  calls = 0
  def tracer(func, *args):
      global calls
      calls += 1 
      print("call %s to %s" % (calls, func.__name__))
      func(*args)
  
  def spam2(a, b, c):
      print(a + b + c)
      
  def main():
      tracer(spam2, 1, 2, 3)
      tracer(spam2, 1, 2, 3)
      tracer(spam2, 1, 2, 3)
  
  if __name__ == "__main__":
      main()
  
  ```

两者对比装饰器版本在调用的时候不需要额外的语法，而且意图比较明显

##### 装饰器状态保持方案 

##### 类错误一：对方法进行装饰

##### 对调用计时

##### 添加装饰器参数



#### 编写类装饰器

类装饰器可以用来管理类自身，或者用来拦截实例创建调用以管理实例。



##### 单例类

由于类装饰器可以用来拦截实例创建调用，因此可以用来管理一个类的所有实例。

如下实现了单例编程模式：它限制每个类只有一个单独的实例

```python
instances = {}

def singleton(aClass):
    def onCall(*args, **kwargs):
        if aClass not in instances:
            instances[aClass] = aClass(*args, **kwargs)
        return instances[aClass]
    return onCall


@singleton
class Person:
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate

@singleton
class Spam:
    def __init__(self, val):
        self.attr = val

def main():
    bob = Person('Bob', 40, 10)
    print(bob.name, bob.pay())
    sue = Person('Sue', 50, 20)
    print(sue.name, sue.pay())

    x = Spam(val=42)
    y = Spam(99)
    print(x.attr, y.attr)

        
if __name__ == "__main__":
    main()
```

**编写替代方案：**

前面是使用全局变量的方式，下面分别用nonlocal语句、函数属性和类的方式各编写了一个版本：

```python
# ===========使用nonlocal方式=========
def singleton2(aClass):
    instance = None
    def onCall(*args, **kwargs):
        nonlocal instance
        if instance == None:
            instances = aClass(*args, **kwargs)
        return instances
    return onCall

# ============使用函数属性==================
def singleton3(aClass):
    def onCall(*args, **kwargs):
        if onCall.instances == None:
            onCall.instances = aClass(*args, **kwargs)
        return onCall.instances
    onCall.instance = None
    return onCall


# =============使用类编写===============
class singleton4:
    def __init__(self, aClass):
        self.aClass = aClass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.aClass(*args, **kwargs)
        return self.instance
```



##### 跟踪对象接口

另一个应用场景：为每个生成的实例扩展接口，以某种方式管理接口的访问





##### 类错误二：保持多个实例

##### 装饰器vs管理器函数

##### 为什么使用装饰器（回顾）





#### 直接管理函数和类

#### 示例： “私有”和“公有”属性

##### 实现私有属性

##### 实现细节一

##### 公有声明的推广

##### 实现细节二

##### 开发问题

##### python不是关于控制



### 第40章 元类

元类 --> 扩展装饰器的代码插入模型

* 装饰器 --> 扩展函数调用、类实例创建调用

* 元类 --> 扩展类的创建

区别:

* 元类装饰器 --> 在被装饰类创建完成之后运行 --> 通常用来：添加在实例创建的时候运行的逻辑

* 元类 --> 在类创建过程中就运行了的 --> 通常用来:管理或扩展类

示例：

​	声明一个元类，告诉python把类对象的创建路由到我们所提供的另外一个类

```python
def extra(self, arg):...

class Extras(type):
    def __init__(Class, classname, superclasses, attributedict):
        if required():
            Class.extra = extra

class Client1(metaclass=Extras):...
class Client2(metaclass=Extras):...
class Client3(metaclass=Extras):...

x = Client1()
x.extra()
```

#### 声明元类

* 在python3中的声明

  ```python
  class Spam(metaclass=Meta)
  
  class Spam(Eggs, metaclass=Meta)
  ```

* 在python2中的声明

  ```python
  class Spam(object):
  	__metaclass__ = Meta
  
  class Spam(Eggs, object):
      __metaclass__ = Meta
  ```

#### 编写元类

元类 --> 用常规的python class 语句和语法编写 --> 唯一的实质区别: 必须遵循type父类所预期的接口

##### 其他元类编程技巧

###### 使用简单的工厂函数

元类并不需要是一个类 --> 如何可调用对象都可用作为元类

如一个简单的对象工程函数

```python
def MetaFunc(classname, supers, classdict):
    print('In MetaOne.new:',  classname, supers, classdict, sep='\n...')
    return type(classname, supers, classdict)


class Eggs:
    pass


print("making class")
class Spam(Eggs, metaclass=MetaFunc):
    data = 1
    def meth(self, arg):
        return self.data + arg

print("making instance")
x = Spam()
print("data:", x.data, x.meth(2))
```

MetaFunc函数 --> 捕获了通常由type对象的\___call\_默认拦截的调用

###### 用普通类重载类创建调用

 普通类重载\__call\__方法 --> 扮演元类

```python
class MetaObj:
    def __call__(self, classname, supers, classdict):
        print('In MetaOne.new:',  classname, supers, classdict, sep='\n...')
        Class = self.__New__(classname, supers, classdict)
        self.__Init__(Class, classname, supers, classdict)
        return Class

    def __New__(self, classname, supers, classdict):
        print('In MetaOne.new:', classname, supers, classdict, sep='\n...')
        return type(classname, supers, classdict)

    def __Init__(self, Class, classname, supers, classdict):
        print("In MetaTwo init:",  classname, supers, classdict, sep='\n...')
        print("...init class object:", list(Class.__dict__.keys()))

class Eggs:
    pass

print("making class")
class Spam(Eggs, metaclass=MetaObj()):
    data = 1
    def meth(self, arg):
        return self.data + arg

print("making instance")
x = Spam()
print("data:", x.data, x.meth(2))
```



###### 用元类重载类创建调用

看不太懂，先略过

#### 继承与实例






## 需要扩展的点:

### 1. 数据库编程

* pickle模块提供了一个简单的对象持久化系统：它能给个让程序轻松地将整个python对象保存和恢复到文件和文件类的对象中。
* ZODB的第三方系统，提供了完整的面向对象数据库系统
* SQLObject可以将关系数据库映射至python的类模块

