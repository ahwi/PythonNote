
def manual_iter(filename):
    with open(filename) as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass


def manual_iter2(filename):
    with open(filename) as f:
        while True:
            line = next(f)
            if line is None:
                break
            print(line, end='')


def main():
    filename = r"C:\Users\Administrator\Desktop\temp\新建文本文档 (6).txt"
    # manual_iter(filename=filename)
    manual_iter2(filename=filename)

if __name__ == "__main__":
    main()

