import re
import reprlib

RE_WORD = re.compile("\w+")

class SentenceV3:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence (%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word
        return


def test_sentence1():
    s = SentenceV3('"The time has come," the Walrus said')
    print(s)
    for word in s:
        print(word)


def main():
    test_sentence1()


if __name__ == '__main__':
    main()
