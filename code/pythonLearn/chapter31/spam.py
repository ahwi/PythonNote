class Spam:
    numInstances = 0
    def __init__(self):
        Spam.numInstances += 1

    def printNumInstances():
        print("Number of instances:", Spam.numInstances)
    printNumInstances = staticmethod(printNumInstances)


if __name__ == "__main__":
    a = Spam()
    Spam.printNumInstances()
    a.printNumInstances()
