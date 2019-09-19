class TestSelf:
    def __init__(self):
        pass
    def __repr__(self):
        return "TestSelf hello"

    def start(self, fn):
        fn(self)

    def pr(self):
        print("hi")


def testCallback(ret):
    ret.pr()


class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def start(self):
        print(f"{self.name} start learning")


def testC():
    a = Student
    print(id(a))

    s = a(name="jack", age="18")
    s.start()
    print(id(s))



if __name__ == "__main__":
    # t = TestSelf()
    # t.start(testCallback)
    testC()
