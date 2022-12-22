from abc import abstractmethod


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        predix = cls.__name__
        index = cls.__counter
        self.storage_name = "{}#{}".format(predix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(AutoStorage):

    def __set__(self, instance, value):
        value = self.validated(value)
        super().__set__(instance, value)

    @abstractmethod
    def validated(self, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    def validated(self, value):
        if value <= 0:
            raise ValueError("value must be > 0")
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validated(self, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("value cannot be empty or blank")
        return value


class EntityMeta(type):
    """元类，用于创建带有验证字段的业务实体"""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)


class Entity(metaclass=EntityMeta):
    """带有验证字段的业务实体"""

