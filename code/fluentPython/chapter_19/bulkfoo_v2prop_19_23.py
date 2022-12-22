
def quantify(storage_name):

    def qtf_getter(instance):
        return instance.__dict__[storage_name]

    def qtf_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qtf_getter, qtf_setter)


class LineItem:
    weight = quantify('weight')
    price = quantify('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


def main():
    nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    print(nutmeg.weight)
    print(nutmeg.price)
    print(sorted(vars(nutmeg).items()))


if __name__ == "__main__":
    main()