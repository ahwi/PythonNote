import time, sys

def timer(label="", trace=True):
    class timer:
        def __init__(self, func):
            self.func = func
            self.alltime = 0

        def __call__(self, *args, **kargs):
            start = time.clock()
            result = self.func(*args, **kargs)
            elapsed = time.clock() - start
            self.alltime += elapsed
            if trace:
                print("%s %s: %.5f, %.5f" % (label, self.func.__name__, elapsed, self.alltime))
            return result
    return timer


