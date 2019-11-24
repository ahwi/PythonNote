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



### 第21章 模块:宏伟蓝图

#### 导读

模块可以由两个语句和一个重要的内置函数进行处理

* import
* from
* imp.reload



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





## 需要扩展的点:

### 1. 数据库编程

* pickle模块提供了一个简单的对象持久化系统：它能给个让程序轻松地将整个python对象保存和恢复到文件和文件类的对象中。
* ZODB的第三方系统，提供了完整的面向对象数据库系统
* SQLObject可以将关系数据库映射至python的类模块

