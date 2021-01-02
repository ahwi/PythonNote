import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                              for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


def test_example():
    # 1. namedtuple 用来构建只有少数属性但是没有方法的对象
    beer_card = Card('7', 'diamonds')
    print(beer_card)

    # 2.1 __len__ 方法提供的: 使用len()函数查看有多少张牌
    deck = FrenchDeck()
    print(len(deck))

    # 2.2 __getitem__ 方法提供的: 抽取指定位置的纸牌
    print(deck[0])
    print(deck[-1])

    # 2.3 随机抽取纸牌：random.choice从一个序列中随机选出一个元素
    from random import choice
    print(choice(deck))
    print(choice(deck))
    print(choice(deck))

    # 2.4 __getitem__ 方法把[]操作交给了self._cards列表 所以支持自动切片操作
    # 2.4.1 查看最上面3张
    print(deck[:3])
    # 2.4.2 只看牌面是A的牌
    print(deck[12::13])

    # 2.5 __getitem__方法让对象变得可迭代
    # 2.5.1 迭代
    for card in deck:
        print(card)

    # 2.5.2 反向迭代
    for card in reversed(deck):
        print(card)

    # 2.6 迭代通常是隐式的，即时没有实现__contains__方法，那么in运算符就会按照顺序做一次迭代搜索
    print(Card('Q', 'hearts') in deck)
    print(Card('7', 'bearts') in deck)

    # 2.7 排序： 2最小、A最大； 黑桃 > 红桃 > 方块 > 梅花
    print("2.7 =================")
    for card in sorted(deck, key=spades_high):
        print(card)




if __name__ == '__main__':
    test_example()
