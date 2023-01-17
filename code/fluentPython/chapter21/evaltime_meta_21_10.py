from evalsupport_21_7 import deco_alpha
from evalsupport_21_7 import MetaAleph


print('<[1]> evaltime_meta module start')


@deco_alpha
class ClassThree():
    print('<[2]> ClassThree body')

    def method_y(self):
        print('<[3]> ClassThree.method_y')


class ClassFour(ClassThree):
    print('<[4]> ClassFour body')

    def method_y(self):
        print('<[5]> ClassFour.method_y')


class ClassFive(metaclass=MetaAleph):
    print('<[6]> ClassFive body')

    def __init__(self):
        print('<[7]> ClassFive.__init__')

    def method_z(self):
        print('<[8]> ClassFive.method_z')


class ClassSix(ClassFive):
    print('<[9]> ClassSix body')

    def method_z(self):
        print('<[10]> ClassSix.method_z')


if __name__ == '__main__':
    print('<[11]> ClassThree tests', 30 * '.')
    three = ClassThree()
    three.method_y()
    print('<[12]> ClassFour tests', 30 * '.')
    four = ClassFour()
    four.method_y()
    print('<[13]> ClassFive tests', 30 * '.')
    five = ClassFive()
    five.method_z()
    print('<[14]> ClassSix tests', 30 * '.')
    six = ClassSix()
    six.method_z()

print('<[15]> evaltime_meta module end')



"""
场景3：在Python控制台中导入evaltime_meta_21_10模块后的输出
λ python3
>>> import evaltime_meta_21_10
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__  # 创建ClassFive时调用了MetaAleph.__init__方法
<[9]> ClassSix body
<[500]> MetaAleph.__init__  # 创建ClassFive的子类ClassSix时也调用了MetaAleph.__init__方法
<[15]> evaltime_meta module end
"""


"""
场景4：在命令行中运行 "python3 evaltime_meta_21_10.py" 后的输出
λ python3 evaltime_meta_21_10.py
<[100]> evalsupport module start
<[400]> MetaAleph body
<[700]> evalsupport module end
<[1]> evaltime_meta module start
<[2]> ClassThree body
<[200]> deco_alpha
<[4]> ClassFour body
<[6]> ClassFive body
<[500]> MetaAleph.__init__
<[9]> ClassSix body
<[500]> MetaAleph.__init__
<[11]> ClassThree tests ..............................
<[300]> deco_alpha:inner_1  # 装饰器依附到ClassThree类上之后，method_y方法被替换成inner_1方法......
<[12]> ClassFour tests ..............................
<[5]> ClassFour.method_y  # 虽然ClassFour是ClassThree的子类，但是没有依附装饰器的ClassFour类却不受影响
<[13]> ClassFive tests ..............................
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2  # MetaAleph类的__init__方法把ClassFive.method_z方法替换成inner_2函数
<[14]> ClassSix tests ..............................
<[7]> ClassFive.__init__
<[600]> MetaAleph.__init__:inner_2  # ClassFive的子类ClassSix也是一样，method_z方法被替换成inner_2函数
<[15]> evaltime_meta module end
"""








