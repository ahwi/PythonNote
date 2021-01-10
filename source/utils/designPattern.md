# 设计模式

## Python之设计模式(B站视频学习)

说明：在B站看的[python之设计模式视频](https://www.bilibili.com/video/BV19541167cn)

### 1. 设计模式与面向对象介绍

**设计模式：**对软件设计中普遍存在（反复出现）的各种问题，所提出的解决方案。每一个设计模式系统地命名、解释和评价面对系统中一个重要的和重复出现的设计。

**经典书籍：**

“四人帮”：《设计模式：可复用面向对象软件的基础》

**面向对象的三大特性：**

* 封装
* 继承
* 多态

**接口：**

若干抽象方法的集合

作用：限制实现接口的类必须按照接口给定的调用方式实现这些方法；对高层模块隐藏了类的内部实现。

例子：支付接口，限制的实现该接口的类需要按照给定的调用方式实现，并隐藏了类的内部实现

`1/interface`

```python
from abc import ABCMeta, abstractmethod


# 接口
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def pay(self, money):
        print("支付宝支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


p = AliPay()
p.pay(100)
```

### 2. 面向对象设计原则

**面向对象设计SOLID原则**

* 开发封闭原则：一个软件实体如类、模块和函数应该对扩展开放，对修改关闭。即软件实体应尽量在不修改原有代码的情况下进行扩展。
* 里氏替换原则：所有引用父类的地方必须能够透明地使用其子类的对象。（比如，同一个方法，子类和父类的传参与返回的数据类型应该一样，不然会导致不同的调用）
* 依赖倒置原则：高层模块不应该依赖底层模块，二者都应该依赖其抽象；抽象不应该依赖细节；细节应该依赖抽象。换而言之，要针对接口编程，而不是针对实现编程。
* 接口隔离原则：使用多个专门的接口，而不使用单一的接口，即客户端不应该依赖那些它不需要的接口
* 单一职责原则：不要存在多于一个导致类变更的原因。通俗的说，即一个类只负责一项职责。



例子：`2/desginPrinciple.py`

接口隔离原则的例子：

```python
from abc import ABCMeta, abstractmethod


# =========接口隔离原则=================
# --------------------------------------
"""
违反接口隔离原则的例子

老虎不会飞，却需要实现fly的方法，不然会报错
"""

class Animal1(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        pass
    
    @abstractmethod
    def swim(self):
        pass
    
    @abstractmethod
    def fly(self):
        pass


class Tigger1(Animal1):
    def walk(self):
        print("老虎走路")
        
    def swim(self):
        print("老虎走路")


# ------------------------------------
"""
修改上面的例子，使其符合接口隔离原则

不要使用单一的总接口，而使用多个专门的接口
"""
class LandAnimal(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        pass


class WaterAnimal(metaclass=ABCMeta):
    @abstractmethod
    def swim(self):
        pass


class SkyAnimal(metaclass=ABCMeta):
    @abstractmethod
    def fly(self):
        pass


class Tiger(LandAnimal, WaterAnimal):
    def walk(self):
        print("老虎走路")
    
    def swim(self):
        print("老虎游泳")
```



**设计模式分类**

* 创建型模式（5种）：工厂方法模式、抽象工厂模式、创建者模式、原型模式、单例模式
* 结构型模式（7种）：适配器模式、桥接模式、组合模式、装饰器模式、外观模式、享元模式、代理模式
* 行为型模式（11种）：解释器模式、责任链模式、命令模式、迭代器模式、中介者模式、备忘录模式、观察者模式、状态模式、策略模式、访问者模式、模板方法模式

### 创建型模式

#### 3. 简单工厂模式(不是23种设计模式之一)

**内容：**不直接向客户端暴露对象创建的实现细节，而是通过一个工程类来负责创建产品类的实例。

**角色：**

* 工厂角色（Creator）
* 抽象产品角色（Product）
* 具体产品角色（Concrete Product）

**优点：**

* 隐藏了对象创建的实现细节
* 客户端不需要修改代码

**缺点：**

* 违反了单一职责原则，将创建逻辑几种到一个工厂类里
* 当添加新产品时，需要修改工厂类代码，违反了开闭原则

**例子：**

`3/factory.py`

```python
from abc import ABCMeta, abstractmethod


# 接口
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def pay(self, money):
        if self.use_huabei:
            print("支付宝花呗支付%d元." % money)
        else:
            print("支付宝余额支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


class PaymentFactory:
    def create_payment(self, method):
        if method == 'aliPay':
            return AliPay()
        elif method == 'wechat':
            return WechatPay()
        elif method == 'huabei':
            return AliPay(use_huabei=True)
        else:
            raise TypeError("No such payment named %s" % method)


# client
pf = PaymentFactory()
p = pf.create_payment('aliPay')
p = pf.create_payment('huabei')
p.pay(100)
```



#### 4. 工厂方法模式

**内容：**定义一个用于创建对象的接口（工厂接口），让子类决定实例化哪一个产品类。

**角色：**

* 抽象工厂角色（Creator）
* 具体工厂角色（Conctete Creator）
* 抽象产品角色（Product）
* 具体产品角色（Concrete Product）

**优点：**

* 每个具体产品都对应一个工程类，不需要修改工程类代码
* 隐藏了对象创建的实现细节

**缺点：**

* 每增加一个具体产品类，就必须增加一个相应的具体工厂类

例子：

`4\factoryMethod.py`

```python
from abc import ABCMeta, abstractmethod


# 接口
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def pay(self, money):
        if self.use_huabei:
            print("支付宝花呗支付%d元." % money)
        else:
            print("支付宝余额支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


class PaymentFactory:
    @abstractmethod
    def create_payment(self):
        pass


class AlipayFactory(PaymentFactory):
    def create_payment(self):
        return AliPay()


class WechatPayFactory(PaymentFactory):
    def create_payment(self):
        return WechatPay()


class HuabeiFactory(PaymentFactory):
    def create_payment(self):
        return AliPay(use_huabei=True)


# client
pf = HuabeiFactory()
p = pf.create_payment()
p.pay(100)
```

#### 5. 抽象工厂模式

**内容：**定义一个工程类接口，让工厂子类来创建一系列相关或依赖的对象

例如：生成一部手机，需要手机壳、CPU、操作系统三类对象进行组装，其中每类对象都有不同的种类。对每个具体工厂，分别生产一部手机所需要的三个对象。

相比工厂方法模式，抽象工厂模式中的每个具体工厂都生产一套产品。

**角色：**

* 抽象工厂角色（Creator）
* 具体工厂角色（Concrete Creator）
* 抽象产品角色（Product）
* 具体产品角色（Concrete Product）
* 客户端（Client）

 **优点：**

* 将客户端与类的具体实现分离
* 每个工厂创建了一个完整的产品系列，使得易于交换产品系列
* 有利于产品的一致性（即产品之间的约束关系）

**缺点：**

* 难以支持新种类的（抽象）产品

例子：

`5/abstractFactory.py`

```python
from abc import abstractmethod, ABCMeta


# ----抽象产品------
class PhoneShell(metaclass=ABCMeta):
    @abstractmethod
    def show_shell(self):
        pass


class CPU(metaclass=ABCMeta):
    @abstractmethod
    def show_cpu(self):
        pass


class OS(metaclass=ABCMeta):
    @abstractmethod
    def show_os(self):
        pass


# -------抽象工厂-----
class PhoneFactory(metaclass=ABCMeta):
    @abstractmethod
    def make_shell(self):
        pass

    @abstractmethod
    def make_cpu(self):
        pass

    @abstractmethod
    def make_os(self):
        pass


# ------具体产品--------
class SmallShell(PhoneShell):
    def show_shell(self):
        print("普通手机小手机壳")


class BigShell(PhoneShell):
    def show_shell(self):
        print("普通手机大手机壳")


class AppleShell(PhoneShell):
    def show_shell(self):
        print("苹果手机壳")


class SnapDragonCPU(CPU):
    def show_cpu(self):
        print("晓龙CPU")


class MediaTekCPU(CPU):
    def show_cpu(self):
        print("联发科CPU")


class AppleCPU(CPU):
    def show_cpu(self):
        print("苹果CPU")


class Android(OS):
    def show_os(self):
        print("Android系统")


class IOS(OS):
    def show_os(self):
        print("IOS系统")


# ---------具体工厂---------------
class MiFactory(PhoneFactory):
    def make_cpu(self):
        return SnapDragonCPU()

    def make_os(self):
        return Android()

    def make_shell(self):
        return BigShell()


class HuaweiFactory(PhoneFactory):
    def make_cpu(self):
        return SnapDragonCPU()

    def make_os(self):
        return Android()

    def make_shell(self):
        return SmallShell()


class IPhoneFactory(PhoneFactory):
    def make_cpu(self):
        return AppleCPU()

    def make_os(self):
        return IOS()

    def make_shell(self):
        return AppleShell()


# 客户端

class Phone:
    def __init__(self, cpu, os, shell):
        self.cpu = cpu
        self.os = os
        self.shell = shell

    def show_info(self):
        print("手机信息")
        self.cpu.show_cpu()
        self.os.show_os()
        self.shell.show_shell()


def make_phone(factory):
    cpu = factory.make_cpu()
    os = factory.make_os()
    shell = factory.make_shell()
    return Phone(cpu, os, shell)


p1 = make_phone(MiFactory())
p1.show_info()


```

#### 6. 建造者模式

**内容：**

将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示

**角色：**

* 抽象构造者（Builder）
* 具体建造者（Concrete Builder）
* 指挥者（Director）
* 产品（Product）

建造者模式与抽象工厂模式相似，也用来创建复杂对象。主要区别是建造者模式着重一步步构造一个复杂对象，而抽象工厂模式着重于多个系列的产品对象。

**优点：**

* 隐藏了一个产品的内部结构和装配过程
* 将构造代码和表示代码分开
* 可以对构造过程进行更精细的控制

示例：

`6/builder.py`

```python
from abc import ABCMeta, abstractmethod


class Player:
    def __init__(self, face=None, body=None, arm=None, leg=None):
        self.face = face
        self.body = body
        self.arm = arm
        self.leg = leg

    def __str__(self):
        return '%s, %s, %s, %s' % (self.face, self.body, self.arm, self.leg)


class PlayerBuilder(metaclass=ABCMeta):
    @abstractmethod
    def build_face(self):
        pass

    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_arm(self):
        pass

    @abstractmethod
    def build_leg(self):
        pass


class SexyGirBuilder(PlayerBuilder):
    def __init__(self):
        self.player = Player()

    def build_face(self):
        self.player.face = "漂亮脸蛋"

    def build_body(self):
        self.player.body = "苗条"

    def build_arm(self):
        self.player.arm = "漂亮胳膊"

    def build_leg(self):
        self.player.leg = "大长腿"


class MonsterBuilder(PlayerBuilder):
    def __init__(self):
        self.player = Player()

    def build_face(self):
        self.player.face = "怪兽脸"

    def build_body(self):
        self.player.body = "怪兽身材"

    def build_arm(self):
        self.player.arm = "长毛的胳膊"

    def build_leg(self):
        self.player.leg = "长毛的腿"


class PlayerDirector:  # 控制组装顺序
    def build_player(self, builder):
        builder.build_body()
        builder.build_face()
        builder.build_arm()
        builder.build_leg()
        return builder.player


# client
builder = SexyGirBuilder()
director = PlayerDirector()
p = director.build_player(builder)
print(p)
```



#### 7. 单例模式

**内容：**

保证一个类只有一个实例，并提供一个访问它的全局访问点

**角色：**

* 单例（Singleton)

**优点：**

* 对唯一实例的受控访问
* 单例相当于全局变量，但防止了命名空间被污染

示例：

`7/singleton`

```python
from abc import abstractmethod, ABCMeta


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class MyClass(Singleton):
    def __init__(self, a):
        self.a = a


a = MyClass(10)
b = MyClass(20)

print(a.a)
print(b.a)
print(id(a), id(b))
```



### 创建型模式小结

* 抽象工厂模式和建造者模式相比于简单工厂模式和工厂方法模式而言更灵活也更复杂
* 通常情况下、设计以简单工厂模式或工厂方法模式开始，当你发现设计需要更大的灵活性时，则向更复杂的设计模式演化。

### 结构型模式

控制多个类进行协同工作

#### 8. 适配器模式

**内容：**

将一个类的接口转换成客户希望的另一个接口。适配器模式使得原本由于接口不兼容而不能在一起工作的那些类可以一起工作。

**两种实现方式：**

* 类适配器：使用多继承
* 对象适配器：使用组合

**角色：**

* 目标接口（Target）
* 待适配的类（Adaptee）
* 适配器（Adapter）

适用场景：

* 想使用一个已经存在的类，而它的接口不符合你的要求
* （对象适配器）想使用一些已经存在的子类，但不可能对每一个都进行子类化以匹配它们的接口。对象适配器可以适配它的父类接口。

**示例：**

```python
from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass


class AliPay(Payment):
    def pay(self, money):
        print("支付宝支付%d元." % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元。" % money)


class BankPay:
    def cost(self, money):
        print("银联支付%d元。" % money)


# # 类适配器
# """
# 将BankPay原先不兼容的cost()接口适配到pay()接口
# """
# class NewBankPay(Payment, BankPay):
#     def pay(self, money):
#         self.cost(money)
#
#
# p = NewBankPay()
# p.pay(100)

class ApplePay:
    def cost(self, money):
        print("苹果支付%d元。" % money)


# 对象适配器
"""
通过组合，将两个不适配的类适配到pay接口
"""
class PaymentAdapter(Payment):
    def __init__(self, payment):
        self.payment = payment

    def pay(self, money):
        self.payment.cost(money)


p = PaymentAdapter(BankPay())
p.pay(100)
```

#### 9. 桥模式

**内容：**

将一个事务的两个维度分离，使其都可以独立地变化。

**角色：**

* 抽象（Abstraction）
* 细化抽象（RefinedAbstraction）
* 实现者（Implementor）
* 具体实现者（ConreteImplementor）

**应用场景：**

当事务有两个维度上的表现，两个维度都可能扩展时。

**优点：**

* 抽象和实现相分离
* 优秀的扩展能力

**示例：**

```python
# ==============不符合设计模式的例子================================
"""
如下创建两个类：Shape形状 Line线
这种方式有个缺点就是不好扩展，在任意一个维多进行扩展时， 需要添加很多类,
比如增加一个五角星类，需要增加很多类，红色的五角星、蓝色的五角星等
"""
# class Shape:
#     pass
#
# class Line(Shape):
#     pass
#
# class Rectangle(Shape):
#     pass
#
# class Circle(Shape):
#     pass
#
# class RedLine(Line):
#     pass
#
# class GreenLine(Line):
#     pass
#
# class BlueLine(Line):
#     pass


# ==================将上面的例子使用桥模式更改===================================
from abc import ABCMeta, abstractmethod


class Shape(metaclass=ABCMeta):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def draw(self):
        pass


class Color(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, shape):
        pass


class Rectangle(Shape):
    name = "长方形"
    def draw(self):
        self.color.paint(self)


class Circle(Shape):
    name = "圆形"
    def draw(self):
        self.color.paint(self)


class Red(Color):
    def paint(self, shape):
        print("红色的%s" % shape.name)


class Green(Color):
    def paint(self, shape):
        print("绿色的%s" % shape.name)


# client
shape = Rectangle(Red())
shape.draw()

shape2 = Circle(Green())
shape2.draw()

```

#### 10. 组合模式

**内容：**

将对象组合成树形结构以表示“部分-整体”的层次结构。组合模式使得用户对单个对象和组合对象的使用具有一致性。

**角色：**

* 抽象组件（Component）
* 叶子组件（Leaf）
* 复合组件（Composite）
* 客户端（Client）













