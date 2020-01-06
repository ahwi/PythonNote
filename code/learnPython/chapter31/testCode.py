import os


# ***********************************
# 函数装饰器
# ***********************************

def decorator1(F):
    print("Hi, i am decorator1")
    return F


def decorator2(F):
    def wrapper(*args):
        print("Hi,i am decorator2")
        F(*args)
    return wrapper


class decorator3:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        print("Hi,i am decorator3")
        self.func(*args)


@decorator3
def func1(x, y):
    print(f"Hi,i am func1.\tx:{x} y:{y}")


class C:
    @decorator2
    def method(self, x, y):
        print(f"Hi,i am C.\tx:{x} y:{y}")


# ***********************************
# 类装饰器
# ***********************************
def decorator4(cls):
    class Wrapper:
        def __init__(self, *args):
            self.wrapped = cls(*args)

        def __getattr__(self, name):
            print("Hi,i am decorator4")
            return getattr(self.wrapped, name)
    return Wrapper


def decorator5(C):
    class Wrapper:
        def __init__(self, *args):
            print("Hi,i am decorator5")
            self.wrapped = C(*args)
    return Wrapper

class Wrapper:pass
def decorator6(C):
    def onCall(*args):
        return Wrapper(C(*args))
    return onCall


@decorator6
class C2:
    def __init__(self, x, y):
        self.attr = 'spam'


def main():
    # func1(5, 6)
    # func1(7, 8)
    # x = C()
    # x.method(5, 6)
    x = C2(6, 7)
    print(x.attr)
    pass



if __name__ == '__main__':
    main()