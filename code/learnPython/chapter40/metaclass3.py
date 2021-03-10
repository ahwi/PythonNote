
def MetaFunc(classname, supers, classdict):
    print('In MetaOne.new:',  classname, supers, classdict, sep='\n...')
    return type(classname, supers, classdict)


class Eggs:
    pass


print("making class")


class Spam(Eggs, metaclass=MetaFunc):
    data = 1
    def meth(self, arg):
        return self.data + arg

print("making instance")
x = Spam()
print("data:", x.data, x.meth(2))
