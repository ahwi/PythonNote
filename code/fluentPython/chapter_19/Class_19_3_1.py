class Class:  # 定义Class类，这个类有两个类属性：data数据属性和prop特性
    data = 'the class data attr'

    @property
    def prop(self):
        return 'the prop value'


def main():
    obj = Class()
    print(vars(obj))  # vars函数返回obj的__dict__属性，表明没有实例属性
    print(obj.data)  # 读取obj.data，读取的是Class.data的值
    obj.data = 'bar'  # 为obj.data赋值，创建一个实例属性
    print(vars(obj))  # 审查实例，查看实例属性
    print(obj.data)  # 获取的是实例属性的值。从obj实例中读取属性时，实例属性data会遮盖类属性data
    print(Class.data)  # Class.data属性的值完好无损
    """
    结果：
    {}
    the class data attr
    {'data': 'bar'}
    bar
    the class data attr
    """

    print("=================================")
    print(Class.prop)  # 直接从Class中读取的prop特性，获取的是特性对象本身，不会允许特性的读值方法
    """
    <property object at 0x000001E7E1708638>
    """
    print(obj.prop)  # 会执行特性的读值方法
    """
    the prop value
    """
    # obj.prop = 'foo'  # 会抛异常
    # """
    # Traceback (most recent call last):
    # ...
    # AttributeError: can't set attribute
    # """
    obj.__dict__['prop'] = 'foo'  # 可以直接把'prop'存入obj.__dict__
    print(vars(obj))
    """
    {'data': 'bar', 'prop': 'foo'}
    """
    print(obj.prop)  # 特性没有被实例属性遮盖
    """
    the prop value
    """
    Class.prop = 'baz'  # 覆盖Class.prop特性， 销毁特性对象
    print(obj.prop)  # Class.prop
    """
    foo
    """

    print("=================================")
    print(obj.data)  # 获取的是实例属性data
    print(Class.data)  # 获取的是类属性data
    Class.data = property(lambda self: 'the "data" prop value')  # 使用新特性覆盖Class.data
    print(obj.data)  # obj.data 被Class.data特性覆盖了
    del Class.data  # 删除特性
    print(obj.data)  # 现在恢复原样，obj.data获取的是实例属性data
    """
    结果:
    bar
    the class data attr
    the "data" prop value
    bar
    """


if __name__ == "__main__":
    main()