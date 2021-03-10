
class MetaOne(type):
    def __new__(meta, classname, supers, classdict):
        print('In MetaOne.new:', meta, classname, supers, classdict, sep='\n...')
        return type.__new__(meta, classname, supers, classdict)


class Eggs:
    pass

print("making class")


class Spam(Eggs, metaclass=MetaOne):
    data = 1
    def meth(self, arg):
        return self.data + arg

print("making instance")
x = Spam()
print("data:", x.data, x.meth(2))
