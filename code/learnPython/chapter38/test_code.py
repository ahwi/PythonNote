
#  1. 装饰器状态保持方案=============
# 1.1 类实例属性
class tracer1:
    def __init__(self, func):
        self.call = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        self.call += 1
        print(self, args, kwargs)
        print("call %s to %s" % (self.call, self.func.__name__))
        # self.func(*args, **kwargs)
        return self.func(*args, **kwargs)


# 1.2 封闭作用域和全局作用域
calls = 0
def tracer2(func):
    def wrapper(*args, **kwargs):
        global calls
        calls += 1
        print("call %s to %s" % (calls, func.__name__))
        func(*args, **kwargs)
    return wrapper


# 1.3 封闭作用域和nonlocal
def tracer3(func):
    calls = 0
    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print("call %s to %s" % (calls, func.__name__))
        func(*args, **kwargs)
    return wrapper

@tracer3
def spam(a, b, c):
    print(a + b + c)


@tracer3
def eggs(x, y):
    print(x ** y)


# ===== 2. 类错误之一：装饰类方法=========
# 2.1 使用嵌套函数来装饰方法
# 2.2 使用描述符装饰方法
class tracer5(object):
    def __init__(self, func):
        self.calls = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"=====")
        self.calls += 1
        print("call %s to %s" % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        print(f"get {instance} {owner} ==")
        return wrapper(self, instance)


class wrapper:
    def __init__(self, desc, subj):
        print(f"wrapper init")
        self.desc = desc
        self.subj = subj

    def __call__(self, *args, **kwargs):
        print(f"wrapper call {self.desc} {self.subj} {args} {kwargs}")
        return self.desc(self.subj, *args, **kwargs)

# 使用嵌套的函数和封闭的作用域引用来实现同样的效果
class tracer6(object):
    def __init__(self, func):
        self.calls = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"=====")
        self.calls += 1
        print("call %s to %s" % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        print(f"get {instance} {owner} ==")
        def wrapper(*args, **kwargs):
            return self(instance, *args, **kwargs)
        return wrapper


class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer6
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
        print(f"giveRaise")

    @tracer6
    def lastName(self):
        return self.name.split()[-1]




def test_code():
    # spam(1, 2, 3)
    # spam(a=4, b=5, c=6)
    # eggs(2, 16)
    # eggs(4, y=4)

    bob = Person('Bob Smith', 50000)
    bob.giveRaise(.25)
    # print("####")
    # bob.giveRaise(.25)
    # print(bob.lastName())


def main():
    test_code()

if __name__ == '__main__':
    main()


