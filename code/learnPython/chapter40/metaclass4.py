
class MetaObj:
    def __call__(self, classname, supers, classdict):
        print('In MetaOne.new:',  classname, supers, classdict, sep='\n...')
        Class = self.__New__(classname, supers, classdict)
        self.__Init__(Class, classname, supers, classdict)
        return Class

    def __New__(self, classname, supers, classdict):
        print('In MetaOne.new:', classname, supers, classdict, sep='\n...')
        return type(classname, supers, classdict)

    def __Init__(self, Class, classname, supers, classdict):
        print("In MetaTwo init:",  classname, supers, classdict, sep='\n...')
        print("...init class object:", list(Class.__dict__.keys()))


class Eggs:
    pass


print("making class")


class Spam(Eggs, metaclass=MetaObj()):
    data = 1
    def meth(self, arg):
        return self.data + arg

print("making instance")
x = Spam()
print("data:", x.data, x.meth(2))
