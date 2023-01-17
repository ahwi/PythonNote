## 异步编程学习



### 参考:

1.  从0到1，Python异步编程的演进之路

   <https://zhuanlan.zhihu.com/p/25228075> 

## 单元测试

比较知名的几种单元测试工具

* unittest 
* unittest2 
* pytest 
* nose 
* doctest

有时间优先学习unittest pytest这两种

### 单元测试之unittest

参考链接：`https://zhuanlan.zhihu.com/p/95907722`

unittest:这是一款受到**JUnit**的启发，与其他语言中的主流单元测试框架有着相似的风格。其支持测试自动化，配置共享和关机代码测试。

#### 简单实例

下面下看一个unittest单元测试实例：

`code/utils/testUnittest/test1.py`

```python
import unittest


# 用于测试的类
class TestClass:
    def add(self, x, y):
        return x + y

    def is_string(self, s):
        return type(s) == str

    def raise_error(self):
        raise KeyError("test.")


# 测试用例
class Case(unittest.TestCase):
    def setUp(self):
        self.test_class = TestClass()

    def test_add_5_5(self):
        self.assertEqual(self.test_class.add(5, 5), 10)

    def test_bool_value(self):
        self.assertTrue(self.test_class.is_string("hello world!"))

    def test_raise(self):
        # 注意这边传递的是函数地址，没有加括号
        self.assertRaises(KeyError, self.test_class.raise_error)

    def tearDown(self):
        del self.test_class


if __name__ == '__main__':
    unittest.main()
```

这里实现了一个用于测试的类`TestClass`，它包含三个方法`add`、`is_string`、`raise_error`

测试用例`Case`类包含了几个需要关注的点：

* 继承

  `unittest`提供一个基类`TestCase`，如果我们要编写一个测试用例，就需要继承这个抽象基类，这样当我们运行测试程序时它会自动的运行这些测试用例。

* 测试方法名称

  测试方法要以`test`开头，这样测试程序能够自动找到要运行的方法。

* `setUp`和`tearDown`

  当一个测试用例开始之前，会先进入`setUp`类，当结束后会进入`tearDown`方法。有点类似构造和析构函数。

  在上面测试用例中，在`setUp`中用于实例化`TestClass`这个要被测试的类，然后在`tearDown`中清理对象。

* 断言

  在上述测试用例中也用到一些用于断言的方法，它们来自于unittest基类，用来检查预期的输出。

执行程序得到的结果：

```bash
λ python3 test1.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

添加详细的输出：

```bash
λ python3 test1.py -v
test_add_5_5 (test1.Case) ... ok
test_bool_value (test1.Case) ... ok
test_raise (test1.Case) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

> 注意：不能按`python3 -m unittest test1.py`这种方式执行，不然会执行两次 

#### 测试套件（TestSuite）

上面的测试用例流程比较固化，只能按照顺序寻找test开头的测试方法，顺序执行。

下面要讲的测试套件能够归档测试用例，让我们按照指定的顺序去执行测试方法。

测试套件代码只需要修改调用的部分：

完整代码参考`code/utils/testUnittest/test2.py`

```python
if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [
        Case('test_raise'),
        Case('test_bool_value'),
        Case('test_add_5_5')
    ]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
```

注意点：

* 初始化套件

  通过`suite = unittest.TestSuite()`来初始化套件

* 添加测试用例

  添加测试用例的两个方法：

  * 使用`suite.addTests()`函数添加一个列表
  * 使用`suite.addTest()`逐个函数添加

* 执行测试用例

  `测试运行器（test runner）`：是一个用于执行和输出测试结果的组件。

  执行器的参数列表如下：

  ```python
  class unittest.TextTestRunner(stream=None, descriptions=True, verbosity=1, failfast=False, buffer=False, resultclass=None, warnings=None, *, tb_locals=False)
  ```

  其中stream可以用于指定输出测试信息到文件，verbosity用于指定输出详细信息。

  然后用运行器运行测试套件即可，结果如下：

  ```bash
  λ python3 test2.py -v 
  test_add_5_5 (test2.Case) ... ok
  test_bool_value (test2.Case) ... ok
  test_raise (test2.Case) ... ok
  
  ----------------------------------------------------------------------
  Ran 3 tests in 0.001s
  
  OK
  ```

#### 跳过测试与预计的失败

示例如下：

完整代码`code/utils/testUnittest/test3.py`

```python
NUM = 1


class SkipCase(unittest.TestCase):

    def setUp(self):
        self.test_class = TestClass()


    @unittest.skip("Skip test.")
    def test_add_5_5(self):
        self.assertEqual(self.test_class.add(5, 5), 10)

    @unittest.skipIf(NUM < 3, "Skiped: the number is too small.")
    def test_bool_value(self):
        self.assertTrue(self.test_class.is_string("hello world!"))

    @unittest.skipUnless(NUM==3, "Skiped: the number is not equal 3.")
    def test_raise(self):
        self.assertRaises(KeyError, self.test_class.raise_error)
```

使用装饰器的方式来跳过测试与预计的失败，常用的主要有3种方法：

* `unittest.skip`：直接跳过测试用例
* `unittest.skipIf`：当调节满足时跳过测试用例
* `unittest.skipUnless`：只有满足某一条件时不跳过，其他的都跳过

上面示例的执行结果：

```bash
λ python3 test3.py -v
test_add_5_5 (test3.SkipCase) ... skipped 'Skip test.'
test_bool_value (test3.SkipCase) ... skipped 'Skiped: the number is too small.'
test_raise (test3.SkipCase) ... skipped 'Skiped: the number is not equal 3.'

----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK (skipped=3)
```

#### 复用测试代码

可以使用`TestCase`来复用测试代码。

（还没仔细了解，后续有时间再了解）



  





































