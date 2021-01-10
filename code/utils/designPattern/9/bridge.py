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

