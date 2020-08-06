class Tracer:
    def __init__(self, aClass):
        self.aClass = aClass

    def __call__(self, *args, **kwargs):
        self.wrapped = self.aClass(*args, **kwargs)
        return self

    def __getattr__(self, item):
        print(f"Trace: " + item)
        return getattr(self.wrapped, item)



@Tracer
class Person:
    def __init__(self, name):
        self.name = name


class T:
    def __init__(self):
        print(f"T: init")

    def __call__(self, *args, **kwargs):
        print(f"T: call")


def main():
    bob = Person("Bob")
    print(bob.name)
    sue = Person("Sue")
    print(sue.name)
    print(bob.name)

    t = T()
    t("")





if __name__ == '__main__':
    main()