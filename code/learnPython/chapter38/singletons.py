instances = {}

def singleton1(aClass):
    def onCall(*args, **kwargs):
        if aClass not in instances:
            instances[aClass] = aClass(*args, **kwargs)
        return instances[aClass]
    return onCall



# ===========使用nonlocal方式=========
def singleton2(aClass):
    instance = None
    def onCall(*args, **kwargs):
        nonlocal instance
        if instance == None:
            instances = aClass(*args, **kwargs)
        return instances
    return onCall

# ============使用函数属性==================
def singleton3(aClass):
    def onCall(*args, **kwargs):
        if onCall.instances == None:
            onCall.instances = aClass(*args, **kwargs)
        return onCall.instances
    onCall.instance = None
    return onCall


# =============使用类编写===============
class singleton4:
    def __init__(self, aClass):
        self.aClass = aClass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.aClass(*args, **kwargs)
        return self.instance



@singleton
class Person:
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate

@singleton
class Spam:
    def __init__(self, val):
        self.attr = val

def main():
    bob = Person('Bob', 40, 10)
    print(bob.name, bob.pay())
    sue = Person('Sue', 50, 20)
    print(sue.name, sue.pay())

    x = Spam(val=42)
    y = Spam(99)
    print(x.attr, y.attr)

        
if __name__ == "__main__":
    main()
