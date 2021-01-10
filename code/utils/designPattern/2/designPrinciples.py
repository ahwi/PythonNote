from abc import ABCMeta, abstractmethod


# =========接口隔离原则=================
# --------------------------------------
"""
违反接口隔离原则的例子

老虎不会飞，却需要实现fly的方法，不然会报错
"""

class Animal1(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        pass

    @abstractmethod
    def swim(self):
        pass

    @abstractmethod
    def fly(self):
        pass


class Tigger1(Animal1):
    def walk(self):
        print("老虎走路")

    def swim(self):
        print("老虎走路")


# ------------------------------------
"""
修改上面的例子，使其符合接口隔离原则

不要使用单一的总接口，而使用多个专门的接口
"""
class LandAnimal(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        pass


class WaterAnimal(metaclass=ABCMeta):
    @abstractmethod
    def swim(self):
        pass


class SkyAnimal(metaclass=ABCMeta):
    @abstractmethod
    def fly(self):
        pass


class Tiger(LandAnimal, WaterAnimal):
    def walk(self):
        print("老虎走路")

    def swim(self):
        print("老虎游泳")

