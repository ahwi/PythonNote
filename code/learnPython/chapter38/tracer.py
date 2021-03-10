

class tracer:
    def __init__(self, func):
        self.calls = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        print(f"get===={instance} | {owner}")
        return wrapper(self, instance)


class wrapper:
    def __init__(self, desc, subj):
        print("wrapper ini====")
        self.desc = desc
        self.subj = subj

    def __call__(self, *args, **kwargs):
        print(f"wrapper call ")
        return self.desc(self.subj, *args, **kwargs)


@tracer
def spam(a, b, c):
    print(a + b + c)


class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay

    @tracer
    def giveRaise(self, percent):
        self.pay *= (1.0 + percent)
        print("giveRaise")

    @tracer
    def lastName(self):
        return self.name.split()[-1]


sue = Person("tome", 1)
print(f"{sue}")
sue.giveRaise(.10)
