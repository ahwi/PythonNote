class wrapper:
    def __init__(self, object):
        self.wrapped = object

    def __getattr__(self, attrname):
        print("Trace:", attrname)
        return getattr(self.wrapped, attrname)


if __name__ == "__main__":
    x = wrapper([1,2,3])
    x.append(4)
