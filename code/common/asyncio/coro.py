

def coro1():
    world = yield "hello"
    yield world
    return world


def coro2():
    print("#2")
    result = yield from coro1()
    print("coro2 result", result)
    return "ffff"


def coro3():
    result = yield from []
    print("fff")
    print(result)
    return "coro3 ret"


class Future:
    def __init__(self):
        self.result = None   # 保存结果
        self._callbacks = []  # 保存对 Future 的回调函数

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)

    def __iter__(self):
        """ 让 Future 对象支持 yield from"""
        yield self  # 产出自己
        return self.result   # yield from 将把 result 值返回作为 yield from 表达式的值


def callback_1(a, b):
    f = Future()

    def on_callback_1():
        f.set_result(a+b)

    on_callback_1()
    c = yield from f
    print("callback1")
    return c


def callback_2(c):
    f = Future()

    def on_callback_2():
        f.set_result(c*2)
    on_callback_2()
    c = yield from f
    return c


def callback_3(c):
    f = Future()

    def on_callback_3():
        f.set_result(c)
    on_callback_3()
    yield from f


def caller_use_yield_from(a, b):
    c1 = yield from callback_1(a, b)
    c2 = yield from callback_2(c1)
    yield from callback_3(c2)
    return c2


def main():
    c = caller_use_yield_from(1, 2)
    f1 = c.send(None)
    f2 = c.send(f1.result)
    f3 = c.send(f2.result)
    try:
        f4 = c.send(None)
    except Exception as e:
        print(e.value)
    # -------------------
    # c3 = coro3()
    # print(c3.send(None))
    # ------------------------
    # print(next(c3))
    # print(next(c3))
    # c2 = coro2()
    # print("#1")
    # print(next(c2))
    # print(c2.send("world"))
    # try:
    #     c2.send(None)
    # except Exception as e:
    #     print("aaaa")
    #     print(e)


if __name__ == '__main__':
    main()
