from array import array
import reprlib
import math


class Vector:
    typecode = 'd'

    def __init__(self, components):
        """
        self._components是“受保护的”实例属性，把Vector的分量保存在一个数组中
        """
        self._components = array(self.typecode, components)

    def __iter__(self):
        """
        为了迭代，使用self._components构建一个迭代器
        """
        return iter(self._components)

    def __repr__(self):
        """
        使用reprlib.repr()函数获取self._components的有限长度表示形式（如array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])）
        """
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __byte__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
