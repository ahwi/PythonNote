"""
统计一个函数被调用的次数，并且针对每次调用打印跟踪信息
"""
# ===========装饰器的方式==============

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


#======普通函数的方式=======
calls = 0
def tracer(func, *args):
    global calls
    calls += 1 
    print("call %s to %s" % (calls, func.__name__))
    func(*args)

def spam2(a, b, c):
    print(a + b + c)


def main():
    # spam(1, 2, 3)
    # spam(1, 2, 3)
    # spam(1, 2, 3)

    tracer(spam2, 1, 2, 3)
    tracer(spam2, 1, 2, 3)
    tracer(spam2, 1, 2, 3)


if __name__ == "__main__":
    main()
