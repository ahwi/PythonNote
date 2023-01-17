"""
使用特性工程函数实现与描述符类Quantity相同的功能
"""

def quantity():
    try:
        quantity.counter += 1
    except Exception:
        quantity.counter = 0

    storage_name = "_{}#{}".format("quantity", quantity.counter)

    def qty_getter(instance):
        return getattr(instance, storage_name)

    def qty_setter(instance, value):
        if value > 0:
            setattr(instance, storage_name, value)
        else:
            raise ValueError("value must be > 0")

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity()
    price = quantity()

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
