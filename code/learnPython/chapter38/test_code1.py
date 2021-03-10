
# =========函数属性======
def tracer(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        print("call %s to %s" % (wrapper.calls, func.__name__))
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@tracer
def spam(a, b, c):
    print(a + b + c)


@tracer
def eggs(x, y):
    print(x ** y)

if __name__ == '__main__':
    spam(1, 2, 3)
    spam(a=4, b=5, c=6)

    eggs(2, 16)
    eggs(4, y=4)
