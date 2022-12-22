import unittest


# 用于测试的类
class TestClass:
    def add(self, x, y):
        return x + y

    def is_string(self, s):
        return type(s) == str

    def raise_error(self):
        raise KeyError("test.")


# 测试用例
class Case(unittest.TestCase):
    def setUp(self):
        self.test_class = TestClass()

    def test_add_5_5(self):
        self.assertEqual(self.test_class.add(5, 5), 10)

    def test_bool_value(self):
        self.assertTrue(self.test_class.is_string("hello world!"))

    def test_raise(self):
        # 注意这边传递的是函数地址，没有加括号
        self.assertRaises(KeyError, self.test_class.raise_error)

    def tearDown(self):
        del self.test_class

suite = unittest.TestSuite()
tests = [
    Case('test_raise'),
    # Case('test_bool_value'),
    Case('test_add_5_5')
]
suite.addTests(tests)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
#if __name__ == '__main__':
#    suite = unittest.TestSuite()
#    tests = [
#        Case('test_raise'),
#        # Case('test_bool_value'),
#        Case('test_add_5_5')
#    ]
#    suite.addTests(tests)
#    runner = unittest.TextTestRunner(verbosity=2)
#    runner.run(suite)
