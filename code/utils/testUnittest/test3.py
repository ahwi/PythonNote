import unittest


# 用于测试的类
class TestClass:
    def add(self, x, y):
        return x + y

    def is_string(self, s):
        return type(s) == str

    def raise_error(self):
        raise KeyError("test.")

NUM = 1


class SkipCase(unittest.TestCase):

    def setUp(self):
        self.test_class = TestClass()


    @unittest.skip("Skip test.")
    def test_add_5_5(self):
        self.assertEqual(self.test_class.add(5, 5), 10)

    @unittest.skipIf(NUM < 3, "Skiped: the number is too small.")
    def test_bool_value(self):
        self.assertTrue(self.test_class.is_string("hello world!"))

    @unittest.skipUnless(NUM==3, "Skiped: the number is not equal 3.")
    def test_raise(self):
        self.assertRaises(KeyError, self.test_class.raise_error)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = [
        SkipCase('test_raise'),
        SkipCase('test_bool_value'),
        SkipCase('test_add_5_5')
    ]
    suite.addTests(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
