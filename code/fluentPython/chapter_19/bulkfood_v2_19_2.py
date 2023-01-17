class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 这里已经用到特性的方法，其名称都与公开属性的名称一样
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('Value must be > 0')


def test():
    walnuts = LineItem('walnuts', 0, 10.00)
    print(walnuts)


if __name__ == "__main__":
    test()