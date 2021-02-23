from array import array
import math


class Vector2d:
    typecode = 'd' # 类属性，在vector2d实例和字节序列之间转换时使用

    def __init__(self, x, y):
        self.__x = float(x)   # 把x和y转成浮点数，尽早捕获错误，以防调用Vector2d函数时传入不当参数
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        """
        把Vector2d实例变成可迭代的对象，这样才能拆包（例如，x, y = my_vector），这个方法的实现方式很简单，直接调用生成器表达式一个接一个产出分量
        """
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        """
        使用{!r}获取各个分量的表示形式，然后插值，构成一个字符串；因为Vector2d实例是可迭代的对象，所以*self会把x和y分量提供给format函数
        """
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        """
        从可迭代的Vector2d实例中可以轻松地得到一个元组，显示一个有序对
        """
        return str(tuple(self))

    def __bytes__(self):
        """
        为了生成字节序列，我们把typecode转换成字节序列，然后迭代Vector2d实例，得到一个数组，再把数组转换成字节序列
        """
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        """
        为了快速比较所有分量，在操作数中构建元组。对Vector2d实例来说，可以这样做，不过会导致一些问题，比如Vector(3, 4) == [3, 4]结果也为True
        """
        return tuple(self) == tuple(other)

    def __abs__(self):
        """
        模是x和y分量构成的直角三角形的斜边长
        """
        return math.hypot(self.x, self.y)

    def __bool__(self):
        """
        使用abs(self)计算模，然后把结果转换成布尔值，因此，0.0是False，非零值是True
        """
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets): # 不用传入self参数；相反通过cls传入类本身
        typecode = chr(octets[0])
        memv = memoryview(octets[1:0]).cast(typecode)
        return cls(*memv)

    # def __format__(self, fmt_spec=''):
        # components = (format(c, fmt_spec) for c in self)
        # return '({}, {})'.format(*components)

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return '({}, {})'.format(*components)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
