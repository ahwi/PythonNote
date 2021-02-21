from collections import Iterable, Iterator
from abc import abstractmethod


class MyIterator(Iterable):
    __slots__ = ()

    @abstractmethod
    def __next__(self):
        raise StopIteration

    @classmethod
    def __subclasshook__(cls, C):
        if cls is MyIterator:
            if (any("__next__" in B.__dict__ for B in C.__mro__) and
                any("__iter__" in B.__dict__ for B in C.__mro__)):
                return True
        return NotImplemented


class Foo:
    def __iter__(self):
        pass


def main():
    # ret = issubclass(Foo, MyIterator)
    # print(ret)
    # f = Foo()
    # ret = isinstance(f, MyIterator)
    # print(ret)
    ret = issubclass(Foo, Iterator)
    print(ret)
    f = Foo()
    ret = isinstance(f, Iterator)
    print(ret)



if __name__ == '__main__':
    main()
