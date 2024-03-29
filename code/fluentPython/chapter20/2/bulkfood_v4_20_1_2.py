class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.store_name = "_{}#{}".format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        return getattr(instance, self.store_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.store_name, value)
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


def main():
    truffle = LineItem('white truffle', 100, 0.5)
    print(truffle.weight)
    print(LineItem.weight)


if __name__ == "__main__":
    main()
