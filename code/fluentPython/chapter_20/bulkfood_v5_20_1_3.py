import model_v5_20_1_3 as model


class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


def main():
    # truffle = LineItem('white truffle', 100, 0.5)
    truffle = LineItem('', 100, 0.5)
    print(truffle.weight)


if __name__ == "__main__":
    main()
