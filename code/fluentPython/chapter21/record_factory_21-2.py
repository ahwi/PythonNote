

def record_factory(cls_name, field_names):
    try:
        file_names = field_names.replace(',', '').split()
    except AttributeError:
        pass
    file_names = tuple(file_names)  # 使用属性名构建元组，这将成为新建类的__slots__属性；此外，这么做还设定了拆包和字符串表示形式中各个字段的顺序

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)

    cls_attrs = dict(__slots__=file_names,  # 组成类属性的字典
                     __init__=__init__,
                     __iter__=__iter__,
                     __repr__=__repr__
                     )
    return type(cls_name, (object,), cls_attrs)  # 调用type构造方法，构建新类 ，然后将其返回


# def main():
#     Dog = record_factory('Dog', 'name weight owner')
#     rex = Dog('rex', 30, )
#
#
# if __name__ == "__main__":
#     main()