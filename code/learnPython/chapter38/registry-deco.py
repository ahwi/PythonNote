# ============将函数或类注册到一个基于字典的注册表中=================
registry = {}


def register(obj):
    registry[obj.__name__] = obj
    return obj


@register
def spam(x):
    return (x ** 2)


@register
def ham(x):
    return (x ** 3)


@register
class Eggs:
    def __init__(self, x):
        self.data = x ** 4

    def __str__(self):
        return str(self.data)


def test_registry():
    print("Registry:")
    for name in registry:
        print(f"name:{registry[name]} ==> {type(registry[name])}")

    print("\nManual calls:")
    print(spam(2))
    print(ham(2))
    x = Eggs(2)
    print(x)

    print(f"\nRegistry calls:")
    for name in registry:
        print(f"name ==> {registry[name](2)}")


# ============= 用装饰器来处理函数属性或者类属性、类方法等====================
def decorate(func):
    func.mark = True
    return func

@decorate
def spam2(a, b):
    return a + b


def annotate(text):
    def decorate1(func):
        print("aaaa")
        func.label = text
        return func
    return decorate1


@annotate("spam data")
def spam3(a, b):
    return a + b


def test2():
    # print(spam2.mark)
    # print(spam3)
    # print(spam3(1, 2), spam3.label)
    pass


def main():
    test2()



if __name__ == '__main__':
    main()

