import re
import reprlib

RE_WORD = re.compile('\w+')


class SentenceV5:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Senetence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))



def test_sentence1():
    s = SentenceV5('"The time has come," the Walrus said')
    print(s)
    for word in s:
        print(word)


def main():
    test_sentence1()


if __name__ == '__main__':
    main()
