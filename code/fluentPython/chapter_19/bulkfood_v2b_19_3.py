class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 这里已经用到特性的方法，其名称都与公开属性的名称一样
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('Value must be > 0')

    weight = property(get_weight, set_weight)


def test():
    walnuts = LineItem('walnuts', 0, 10.00)
    print(walnuts)


if __name__ == "__main__":
    test()
