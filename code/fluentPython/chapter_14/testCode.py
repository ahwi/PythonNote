import re
import reprlib

RE_WORD = re.compile("\w+")


class Sentence1:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)


def test_sentence1():
    s = Sentence1('"The time has come," the Walrus said')
    print(s)
    for word in s:
        print(word)
    # print(list(s))
    # print(s[0])
    # print(s[5])
    # print(s[-1])


def main():
    test_sentence1()
    f = open("aaa", "w")
    f.__enter__()




if __name__ == '__main__':
    main()
