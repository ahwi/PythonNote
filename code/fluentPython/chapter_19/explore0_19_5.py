from collections import abc


class FrozenJSON:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):  # obj是映射，那就构建一个FrozenJSON对象
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # 如果是MutableSequence对象，必然是一个列表，因此把每个元素递归的传递给.build()方法，构建一个列表
            return [cls.build(item) for item in obj]
        else:
            return obj
